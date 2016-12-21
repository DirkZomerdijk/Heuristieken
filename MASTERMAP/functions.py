# Fish 'n Chips     Laila Blomer, Dirk Zomerdijk, Anna Vos
#
# Heuristieken
# Case: Chips & Circuits
#
# functions.py

import random
from collections import Counter
from astar import *
from collections import defaultdict

def sort_on_distance(chip):
    '''
    takes chip and returns netlist sorted by distance between gates.
    :param chip: chip object
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
        netlength += len(remove.path)

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
            path, x = astar(chip, net.start, net.end, False, True, False)

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


def remove_obstacle(chip, closedset, start, end, nets_removed, no_path):
    '''
    :param chip: Chip object
    :param closedset: set with nodes in the closedset of A*
    :param start: Gate object
    :param end:
    :param nets_removed:
    :param no_path:
    :return:
    '''
    length = 0
    kids, coordinates = find_obstacles(chip, closedset)
    netpointer = None

    # remove specific obstacle
    if no_path == 1:
        netpointer = random.choice(kids)

    # remove selective obstacle
    elif no_path == 3:
        # check length for every child to end gate
        for i in xrange(len(kids)):
            kids[i].manhattan = abs(coordinates[i][0] - chip.gates[end].coordinate[0]) + abs(
                coordinates[i][1] - chip.gates[end].coordinate[1]) + abs(
                coordinates[i][2] - chip.gates[end].coordinate[2])
        # select child with lowest manhattan score
        netpointer = min(kids, key=lambda x: x.manhattan)

    # remember net to be removed
    nets_removed.append((netpointer.start, netpointer.end))
    length -= (len(netpointer.path) + 1)

    # remove net
    chip.removeNet(netpointer)

    # retry finding path
    path, x = astar(chip, chip.gates[start], chip.gates[end], True, False, True)

    # if again "no path found" remove another obstacle
    if path == "no path found" or path == "switch gates":
        return remove_obstacle(chip, x, start, end, nets_removed, no_path)

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