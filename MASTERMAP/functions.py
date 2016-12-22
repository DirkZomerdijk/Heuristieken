# Fish 'n Chips     Laila Blomer, Dirk Zomerdijk, Anna Vos
#
# Heuristieken
# Case: Chips & Circuits
#
# functions.py


from collections import Counter
from astar import *
from collections import defaultdict
from visualizer import *
from chip import *
import random
import datetime


def sort_on_distance(chip):
    '''
    takes chip and returns netlist sorted by distance between gates.
    :param chip: Chip object
    :return: netlist sorted on longest to shortest distance between the start and end gate.
    '''
    x = defaultdict(list)
    temp = []
    for start, end in chip.netlist:
        length = manhattan(chip.gates[start], chip.gates[end])
        x[length].append((start, end))

    for values in x.values():
        for start_end in values:
            temp.append(start_end)
    return temp


def sort_on_connections(chip):
    '''
    :param chip: Chip object
    :return: returns netlist sorted on amount of gate connections
    '''
    tempnetlist = chip.netlist
    sortednetlist = []
    temp = []

    for start, end in chip.netlist:
        temp.append(start)
        temp.append(end)
    temp = Counter(temp)

    for i in range(len(temp)):
        x = max(temp.iterkeys(), key =(lambda key: temp[key]))

        for start, end in tempnetlist:
            if x == start or x == end:
                sortednetlist.append([start, end])
                tempnetlist.remove([start, end])
            del temp[x]

    return sortednetlist


def remove_random_nets(chip, amount):
    '''
    function removes random nets from the chip.
    :param chip: Chip object
    :param amount: amount of nets to be removed
    :return: list with start and end gates to be placed (again) on the chip, and the length of the removed nets
    '''
    temp = []
    removed = []
    netlength = 0

    # get random nets and remove them from the chip
    for i in range(amount):
        # get random net
        remove = random.choice(chip.nets)
        netlength += len(remove.path) + 2

        temp.append((remove.start, remove.end))

        # remove net
        chip.removeNet(remove)

    for start, end in temp:
        startco = 0
        endco = 0
        # get gate numbers corresponding to net start and end coordinates
        for i in range(len(chip.gates)):
            # get start gate number
            if start.coordinate == chip.gates[i].coordinate:
                startco = i

            # get end gate number
            if end.coordinate == chip.gates[i].coordinate:
                endco = i

        removed.append((startco, endco))

    return removed, netlength


def make_shorter(chip, net_length):
    '''
    function that removed nets and checks if there is a shorter path.
    :param chip: Chip object WITH complete netlines
    :return: chip, netlength
    '''
    versions = {}
    versions[net_length] = chip
    lengths = []

    # for set amount of times, relay nets
    for runs in xrange(50):
        new_length = 0

        for net in chip.nets:
            # remove net
            chip.removeNet(net)

            # find shortest path
            path, x = astar(chip, net.start, net.end, restrictions=False, switch=True, up=False)

            # get coordinates new path
            new_net = []
            for node in path:
                new_net.append(node.coordinate)

            # place net
            chip.placeNet(net.start, net.end, new_net)

            # update return variable
            new_length += len(path) + 1

        # save new chip version
        versions[new_length] = chip
        lengths.append(new_length)

    # find shortest length
    shortest = min(lengths)

    return versions[shortest], shortest


def find_obstacles(chip, closedset):
    '''
    Function that collects all Nets objects surrounding the closedset
    :param chip: Chip object
    :param closedset: set with nodes in the closedset of A*
    :return: returns children of nodes in the closedset who are Nets objects
    '''
    coordinates = []
    children = []

    for node in closedset:
        # get coordinates
        x, y, z = node.coordinate

        # define child coordinates
        child_options = [[x - 1, y, z], [x + 1, y, z], [x, y - 1, z], [x, y + 1, z], [x, y, z - 1], [x, y, z + 1]]
        parameters = [chip.width, chip.height, chip.layer]

        # select nodes surrounding closed set with value "net"
        for i in xrange(6):
            j = int(math.floor(i / 2))
            if child_options[i][j] in xrange(parameters[j]) \
                    and chip.layers[child_options[i][2]].grid[child_options[i][0], child_options[i][1]] != 'free' \
                    and chip.layers[child_options[i][2]].grid[child_options[i][0], child_options[i][1]].value == 'net':
                # append pointers to net objects
                children.append(chip.layers[child_options[i][2]].grid[child_options[i][0], child_options[i][1]])
                # append coordinates
                coordinates.append(child_options[i])

    return children, coordinates


def remove_obstacle(chip, closedset, start, end, nets_removed):
    '''
    :param chip: Chip object
    :param closedset: set with nodes in the closedset of A*
    :param start: Gate object
    :param end: Gate object
    :param nets_removed: List with Nets pointers to be removed
    :return: returns nets_removed, and netlenght of net between start and end
    '''
    length = 0
    kids, coordinates = find_obstacles(chip, closedset)

    # remove specific obstacle
    netpointer = random.choice(kids)

    # remember net to be removed
    nets_removed.append((netpointer.start, netpointer.end))
    length -= (len(netpointer.path) + 1)

    # remove net
    chip.removeNet(netpointer)

    # retry finding path
    path, x = astar(chip, chip.gates[start], chip.gates[end], restrictions=True, switch=False, up=True)

    # if again "no path found" remove another obstacle
    if path == "no path found" or path == "switch gates":
        return remove_obstacle(chip, x, start, end, nets_removed)

    # if path found
    else:
        new_net = []

        # append coordinates of new net
        for node in path:
            new_net.append(node.coordinate)

        # place net on the chip
        chip.placeNet(chip.gates[start], chip.gates[end], new_net)

        length += len(path) + 1

        return nets_removed, length


def run_algorithm(width, height, layer, grid_file, netlist_file, no_path, sorting, visualize):
    '''
    :param width: integer, deciding the width of the print
    :param height: integer, deciding the height of the print
    :param layer: integer, deciding the amount of layers are added to the print
    :param grid_file: text file containing coordinates of gates on the print
    :param netlist_file: text file containing start and end gatenumber of all nets from 1 netlist
    :param no_path: string, defines which removal method is used
    :param sorting: string, defines which sorting method of the netlist is used
    :param visualize: boolean, if true the chip will be visualised in 3D after completion
    :return: returns total runs of A*, running time, netlength after completion and netlength after 'make_shorter' function
    '''

    time_start = datetime.datetime.now()
    chip = Chip(width, height, layer, grid_file, netlist_file)

    # define return variables
    total_length = 0
    total_nets = 0
    total_runs = 0
    indexer = 0

    # sorting method
    if sorting == 'on_connections':
        # sort netlist on amount of connections per gate from high to low
        sorted_netlist = sort_on_connections(chip)

    if sorting == 'on_connections_reverse':
        # sort netlist on amount of connections per gate from low to high
        sorted_netlist = sort_on_connections(chip)[::-1]

    if sorting == 'on_distance_reverse':
        # sort netlist on distance from short to long
        sorted_netlist = sort_on_distance(chip)

    if sorting == 'on_distance':
        # sort netlist on distance from long to short
        sorted_netlist = sort_on_distance(chip)[::-1]

    netlist_length = len(sorted_netlist)

    # search path
    for start, end in sorted_netlist:
        # run A* algorithm
        path, closedset = astar(chip, chip.gates[start], chip.gates[end], restrictions=True, switch=True, up=True)

        # update return variable
        total_runs += 1
        indexer += 1
        # for selective remove of obstacles to avoid infinite loop
        if netlist_length - total_nets < 2 and no_path == 3:
            no_path = 1

        # if no path is found
        if path == 'no path found':
            Visualizer(chip).start()
            # remove random obstacles
            if no_path == 'random':
                # get 3 random nets to be removed and return netlength
                removed, netlength = remove_random_nets(chip, 3)

                # add removed nets to queue
                for net in removed:
                    sorted_netlist.append(net)
                    total_nets -= 1

                # add current to queue
                sorted_netlist.append((start, end))

                # update return variable
                total_length -= netlength

            # remove specific obstacles
            else:
                nets_removed = []
                removed, netlength = remove_obstacle(chip, closedset, start, end, nets_removed)
                total_nets += 1
                total_length += netlength

                # append removed nets to queue
                for start, end in removed:
                    start_coordinate = 0
                    end_coordinate = 0

                    for i in xrange(len(chip.gates)):
                        if start.coordinate == chip.gates[i].coordinate:
                            start_coordinate = i

                        if end.coordinate == chip.gates[i].coordinate:
                            end_coordinate = i

                    sorted_netlist.append((start_coordinate, end_coordinate))

                    # update return variables
                    total_nets -= 1
                    total_runs += 1

        # if closed set of astar is larger than free nodes / 2
        elif path == 'switch gates':
            sorted_netlist.insert(indexer, (end, start))

        # if path is found
        else:
            print "hallo laila"
            # get coordinates from net
            new_net = []
            for node in path:
                new_net.append(node.coordinate)

            # place net path on the chip
            chip.placeNet(chip.gates[start], chip.gates[end], new_net)

            # update return variable
            total_nets += 1
            total_length += len(path) + 1
    Visualizer(chip).start()
    # replace all nets
    chip, new_length = make_shorter(chip, total_length)

    # collect time
    time_end = datetime.datetime.now()

    # visualize chip
    if visualize:
        Visualizer(chip).start()

    return total_runs, total_length, new_length, time_end - time_start
