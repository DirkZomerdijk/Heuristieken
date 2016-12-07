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


def Runastar2(width, height, layer):
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
            path = astar2(chip, chip.gates[start], chip.gates[end])
            total_runs += 1

            # if no path if found
            if path == 'no path found':
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
                # print 'net number:', total_nets
                # print 'path length:', len(path)

    print 'Total net length:', total_length
    print 'Amount of nets:', total_nets
    print 'Total runs of A*', total_runs
    Visualizer(chip).start()

    newlength = total_length + 1
    while newlength < total_length:
        total_length = newlength
        chip, newlength = makeShorter(chip, total_length)

    print 'New net length:', newlength
    Visualizer(chip).start()


    # function that takes the chip with complete nets, starts removing one net, and adding it again.
    # Checking after each cycle if the total net length becomes less > if so, keep the new net.
def makeShorter(chip, netlength):
    '''
    function that removed nets and checks if there is a shorter path.
    :param chip: Chip object WITH complete netlines
    :return: chip, netlength
    '''
    # new_netlength = netlength + 1

    # while new_netlength > netlength:
    # netlength = new_netlength
    new_netlength = 0
    for net in chip.nets:
        start = net.start
        end = net.end
        chip.removeNet(net)

        path = astar2(chip, start, end)

        newnet = []

        # get coordinates from net
        for node in path:
            newnet.append(node.coordinate)
        # place net on the grid
        chip.placeNet(start, end, newnet)

        new_netlength += len(path)
    print 'netlength old:', netlength
    print 'netlength new:', new_netlength

    return chip, new_netlength



# Runsearch(13, 18, 8)
# Runastar(13, 18, 8)
Runastar2(13, 18, 8)
# Runastar2(17, 18, 8)

