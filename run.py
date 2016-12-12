from visualizer import *
from search import *
from astar import *
from chip import *
from astar2 import *

def Runsearch(width, height, layer):
    chip = Chip(width, height, layer, GATESFILE, NETLISTS)

    for start, end in chip.netlist:
        Search(chip, chip.gates[start], chip.gates[end])

    # array = [(1, 1, 1), (1, 2, 1), (1, 3, 1), (1, 3, 2), (1, 4, 2), (1, 4, 1), (1, 5, 1), (1, 5, 0)]
    # chip.placeNet(chip.gates[0], chip.gates[1], array)

    Visualizer(chip).start()

def Runastar(width, height, layer):
    chip = Chip(width, height, layer, GATESFILE, NETLISTS)
    total_length = 0
    total_nets = 0

    # sort netlist
    sort = sortNetlist(chip)

    # search path
    for start, end in sort.values():
        path = astar(chip, chip.gates[start], chip.gates[end])
        total_nets += 1
        net = []
        for node in path:
            net.append(node.coordinate)
        chip.placeNet(chip.gates[start], chip.gates[end], net)

        total_length += len(path)

        Visualizer(chip).start()

    print 'Total net length: ' + total_length + '\nAmount of nets: ' + total_nets


def Runastar2(width, height, layer, nopath):
    chip = Chip(width, height, layer, GATESFILE, NETLISTS)
    total_length = 0
    total_nets = 0
    total_runs = 0

    # sort netlist on length between start and end
    # sorted = sortOnConnections(chip)
    sorted = sortNetlist(chip)

    # search path
    for values in sorted:
        for start, end in values:
            # run A* algorithm
            path, closedset = astar2(chip, chip.gates[start], chip.gates[end], True)
            total_runs += 1

            # if no path is found
            if path == 'no path found':
                if nopath == 1:
                    print 'no path found'
                    removed, netlength = deleteNet(chip, closedset)

                    values.append((start, end))
                    total_length -= netlength

                    for start, end in removed:
                        startco = 0
                        endco = 0
                        for i in range(len(chip.gates)):
                            if start.coordinate == chip.gates[i].coordinate:
                                startco = i
                            if end.coordinate == chip.gates[i].coordinate:
                                endco = i
                        sorted[-1].append((startco, endco))
                        print startco, endco
                        total_nets -= 1

                if nopath == 2:

                    # get 3 random nets to be removed and length of those nets
                    removed, netlength = removeRandomNets(chip, 4)

                    # place removed nets again in queue to be placed on the grid
                    for netlist in removed:
                        sorted[-1].append(netlist)
                        total_nets -= 1

                    # place current start and end gate again in the queue
                    sorted[-1].append((start, end))

                    # subtract removed length of removed nets from total length of nets
                    total_length -= netlength

            elif path == 'switch gates':
                print 'switch gates'
                values.append((end, start))

            # else: path is found
            else:
                print 'path found'
                total_nets += 1
                net = []

                # get coordinates from net
                for node in path:
                    net.append(node.coordinate)
                # place net on the grid
                chip.placeNet(chip.gates[start], chip.gates[end], net)

                total_length += len(path) + 2
                # print 'net number:', total_nets
                # print 'path length:', len(path)

    print 'Total net length:', total_length
    print 'Amount of nets:', total_nets
    print 'Total runs of A*', total_runs
    Visualizer(chip).start()

    #
    # new_length = total_length + 1
    # while new_length < total_length:
    #     total_length = new_length
    #     chip, new_length = makeShorter(chip, total_length)
    chip, new_length = makeShorter(chip, total_length)

    print 'New net length:', new_length
    Visualizer(chip).start()


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
    for runs in range(50):
        new_length = 0

        # for each net in net list
        for net in chip.nets:
            # remove net
            chip.removeNet(net)

            #find shortest path
            path = astar2(chip, net.start, net.end, False)
            new_net = []
            for node in path[0]:
                new_net.append(node.coordinate)

            # place net
            chip.placeNet(net.start, net.end, new_net)
            new_length += len(path) + 2

        # after relaying all nets, save chip to paths by key value of length
        paths[new_length] = chip
        lengths.append(new_length)

    # find shortest of lengths
    shortest = min(lengths)

    return paths[shortest], shortest


def deleteNet(chip, closedset):
    net = []
    length = 0
    for node in closedset:
        print node.coordinate
        if node.value == '[--]':
            x, y, z = node.coordinate
            children = []

            options = [[x - 1, y, z], [x + 1, y, z], [x, y - 1, z], [x, y + 1, z], [x, y, z - 1], [x, y, z + 1]]

            for i in range(6):
                if chip.layers[options[i][2]].grid[options[i][0], options[i][1]] != 'free' and \
                                chip.layers[options[i][2]].grid[options[i][0], options[i][1]].value == 'net':
                    children.append(chip.layers[options[i][2]].grid[options[i][0], options[i][1]])

            if children:
                for netpointer in children:
                    if netpointer == 'net':
                        net.append((netpointer.start, netpointer.end))
                        length += len(netpointer.path)
                        chip.removeNet(chip, netpointer)

                return net, length


runs = 0
# Runsearch(13, 18, 8)
# Runastar(13, 18, 8)
specific = 1
random = 2
Runastar2(13, 18, 8, random)
# Runastar2(13, 18, 8, specific)
# Runastar2(17, 18, 8)

