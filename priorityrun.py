from visualizer import *
from astar2 import *
from chip import *
from search import *
from random import choice
import datetime


def Runastar2(width, height, layer, nopath):
    a = datetime.datetime.now()
    chip = Chip(width, height, layer, GATESFILE, NETLISTS)
    total_length = 0
    total_nets = 0
    total_runs = 0
    indexer = 0

    # sort netlist on length between start and end
    sorted = sortOnConnections(chip)
    netlist_length = len(sorted)

    # sorted = sortNetlist(chip)
    # search path
    for start, end in sorted:
        # run A* algorithm
        # if total_nets > 5:
        path, closedset = astar2(chip, chip.gates[start], chip.gates[end], True, True, True)
        # else:
        # path, closedset = astar2(chip, chip.gates[start], chip.gates[end], True, True, False)

        total_runs += 1
        indexer += 1

        # if no path is found
        if path == 'no path found':
            b = datetime.datetime.now()
            new_length = 0
            return total_nets, total_runs, total_length, new_length, b - a

        elif path == 'switch gates':
            # print 'switch gates'
            sorted.insert(indexer, (end, start))

        # else: path is found
        else:
            # print 'path found'
            total_nets += 1
            net = []

            # get coordinates from net
            for node in path:
                net.append(node.coordinate)
            # place net on the grid
            chip.placeNet(chip.gates[start], chip.gates[end], net)
            # Visualizer(chip).start()

            total_length += len(path) + 1

        # print 'net number:', total_nets
    #
    # print 'Total net length:', total_length
    # print 'Amount of nets:', total_nets
    # print 'Total runs of A*', total_runs
    # Visualizer(chip).start()

    chip, new_length = makeShorter(chip, total_length)

    # print 'New net length:', new_length
    # Visualizer(chip).start()

    b = datetime.datetime.now()

    return total_nets, total_runs, total_length, new_length, b - a

    # function that takes the chip with complete nets, starts removing one net, and adding it again.
    # Checking after each cycle if the total net length becomes less > if so, keep the new net.
def makeShorter(chip, net_length):
    '''
    function that removed nets and checks if there is a shorter path.
    :param chip: Chip object WITH complete netlines
    :return: chip, netlength
    '''
    paths = {}
    paths[net_length] = chip
    lengths = []

    # for set amount of times, relay nets
    for runs in xrange(50):
        new_length = 0

        # for each net in net list
        for net in chip.nets:
            # remove net
            chip.removeNet(net)
            # Visualizer(chip).start()

            #find shortest path
            path, x = astar2(chip, net.start, net.end, False, True, False)
            new_net = []
            for node in path:
                new_net.append(node.coordinate)

            # place net
            chip.placeNet(net.start, net.end, new_net)
            # Visualizer(chip).start()
            new_length += len(path) + 1

        # after relaying all nets, save chip to paths by key value of length
        paths[new_length] = chip
        lengths.append(new_length)

    # find shortest of lengths
    shortest = min(lengths)

    return paths[shortest], shortest


def deleteNet(chip, closedset):
    coordinates = []
    children = []
    for node in closedset:
        # print node.coordinate
        x, y, z = node.coordinate

        options = [[x - 1, y, z], [x + 1, y, z], [x, y - 1, z], [x, y + 1, z], [x, y, z - 1], [x, y, z + 1]]
        parameters = [chip.width, chip.height, chip.layer]

        for i in xrange(6):
            j = int(math.floor(i / 2))
            if options[i][j] in xrange(parameters[j]) and chip.layers[options[i][2]].grid[options[i][0], options[i][1]] != 'free' and chip.layers[options[i][2]].grid[options[i][0], options[i][1]].value == 'net':
                children.append(chip.layers[options[i][2]].grid[options[i][0], options[i][1]])
                coordinates.append(options[i])


            # if chip.layers[options[i][2]].grid[options[i][0], options[i][1]] != 'free' and chip.layers[options[i][2]].grid[options[i][0], options[i][1]].value == 'net':
            #     children.append(chip.layers[options[i][2]].grid[options[i][0], options[i][1]])

    return children, coordinates


def removeobstacle(chip, closedset, start, end, net, nopath):
    length = 0
    kids, coordinates = deleteNet(chip, closedset)

    if not kids:
        Visualizer(chip).start()

    # print "end ", chip.gates[start].coordinate
    # print "start ", chip.gates[end].coordinate
    netpointer = 0
    if nopath  == 1:
        netpointer = choice(kids)
    elif nopath == 3:
        for i in xrange(len(kids)):
            kids[i].manhattan = abs(coordinates[i][0] - chip.gates[end].coordinate[0]) + abs(coordinates[i][1] - chip.gates[end].coordinate[1]) + abs(coordinates[i][2] - chip.gates[end].coordinate[2])
        netpointer = min(kids, key=lambda x: x.manhattan)

    # kids.remove(netpointer)
    # print netpointer.start.coordinate, netpointer.end.coordinate
    net.append((netpointer.start, netpointer.end))
    length -= (len(netpointer.path) + 1)
    chip.removeNet(netpointer)

    path, x = astar2(chip, chip.gates[start], chip.gates[end], True, False, True)

    if path == "no path found" or path == "switch gates":
        return removeobstacle(chip, x, start, end, net, nopath)

    else:
        # print 'alternative path found'
        newnet = []

        # get coordinates from net
        for node in path:
            newnet.append(node.coordinate)
        # place net on the grid
        chip.placeNet(chip.gates[start], chip.gates[end], newnet)

        length += len(path) + 1

        return net, length

abc = 1

# Runsearch(13, 18, 8)
# Runastar(13, 18, 8)
specific = 1
random = 2
more_specific = 3

# Runastar2(13, 18, 8, random)
# Runastar2(17, 18, 8, specific)
# Runastar2(17, 18, 8, random)

runs = 1


###############################################################################################################
# RUNNING 100 RUNS OF RUNASTAR ALGORITHM

# netlist 1
runs_1 = []
length_1 = []
newlength_1 = []
time_1 = []
for i in xrange(runs):
    GATESFILE = open('Heuristieken/txtfiles/print1.txt', 'r')
    NETLISTS = open('Heuristieken/txtfiles/netlist1.txt', 'r')
    total_runs, total_length, new_length, time = Runastar2(13, 18, 8, specific)
    runs_1.append(total_runs)
    length_1.append(total_length)
    newlength_1.append(new_length)
    time_1.append(time.total_seconds())
    print i

print 'MORE SPECIFIC, netlist1:'
print 'runs', runs_1
print 'length', length_1
print 'newlength', newlength_1
print 'time', time_1
