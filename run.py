from visualizer import *
from search import *
from astar import *
from tester import *
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


def Runastar2(width, height, layer):
    chip = Chip(width, height, layer, GATESFILE, NETLISTS)
    total_length = 0
    total_nets = 0

    # sort netlist on length between start and end
    sort = sortNetlist(chip)

    # search path
    for values in sort.values():
        for start, end in values:
            # run A* algorithm
            path = astar2(chip, chip.gates[start], chip.gates[end])

            # if no path if found
            if path == 'no path found':
                # get 3 random nets to be removed and length of those nets
                removed, netlength = removeRandomNets(chip, 3)

                # place removed nets again in queue to be placed on the grid
                for netlist in removed:
                    sort[max(sort.keys())].append(netlist)
                    total_nets -= 1

                # place current start and end gate again in the queue
                sort[max(sort.keys())].append((start, end))

                # subtract removed length of removed nets from total length of nets
                total_length -= netlength

            # else: path is found
            else:
                total_nets += 1
                net = []

                # get coordinates from net
                for node in path:
                    net.append(node.coordinate)
                # place net on the grid
                chip.placeNet(chip.gates[start], chip.gates[end], net)

                total_length += len(path)
                print 'net number:', total_nets
                print 'path length:', len(path)

    print 'Total net length:', total_length
    print 'Amount of nets:', total_nets
    Visualizer(chip).start()



# Runsearch(13, 18, 8)
# Runastar(13, 18, 8)
Runastar2(13, 18, 8)

