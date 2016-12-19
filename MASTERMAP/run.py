from functions import *
from visualizer import *
from astar import *
from chip import *
from random import choice
import datetime

def run_algorithm(width, height, layer, no_path):
    time_start = datetime.datetime.now()
    chip = Chip(width, height, layer, GATESFILE, NETLISTS)

    # define return variables
    total_length = 0
    total_nets = 0
    total_runs = 0
    indexer = 0

    # sort netlist on amount of connections per gate from high to low
    sorted = sortOnConnections(chip)

    # sort netlist on amount of connections per gate from low to high
    # sorted = sortOnConnections(chip)[::-1]

    # sort netlist on distance from short to long
    # sorted = sortNetlist(chip)

    # sort netlist on distance from long to short
    # sorted = sortNetlist(chip)[::-1]

    netlist_length = len(sorted)

    # search path
    for start, end in sorted:
        # run A* algorithm
        path, closedset = astar(chip, chip.gates[start], chip.gates[end], True, True, True)

        # update return variable
        total_runs += 1
        indexer += 1
        # for selective remove of obstacles to avoid infinite loop
        if netlist_length - total_nets < 2 and no_path == 3:
            no_path = 1

        # if no path is found
        if path == 'no path found':
            # remove random obstacles
            if no_path == 2:
                # get 3 random nets to be removed and return netlength
                removed, netlength = removeRandomNets(chip, 3)

                # add removed nets to queue
                for net in removed:
                    sorted.append(net)
                    total_nets -= 1

                # add current to queue
                sorted.append((start, end))

                # update return variable
                total_length -= netlength

            # remove specific obstacles
            else:
                nets_removed = []
                removed, netlength = remove_obstacle(chip, closedset, start, end, nets_removed, no_path)
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
                    sorted.append((start_coordinate, end_coordinate))

                    # update return variables
                    total_nets -= 1
                    total_runs += 1

        # if closed set of astar is larger than free nodes / 2
        elif path == 'switch gates':
            sorted.insert(indexer, (end, start))

        # if path is found
        else:
            # get coordinates from net
            net_path = [net_path.append(node.coordinate) for node in path]

            # place net path on the chip
            chip.placeNet(chip.gates[start], chip.gates[end], net_path)

            # update return variable
            total_nets += 1
            total_length += len(path) + 1

    # replace all nets
    chip, new_length = make_shorter(chip, total_length)

    # collect time
    time_end = datetime.datetime.now()

    return total_runs, total_length, new_length, time_end - time_start


###############################################################################################################
# RUNNING 100 RUNS OF RUNASTAR ALGORITHM

specific = 1
random = 2
more_specific = 3

# run_algorithm(13, 18, 8, random)
# run_algorithm(17, 18, 8, specific)
# run_algorithm(17, 18, 8, random)

runs = 100

# netlist 1
runs_1 = []
length_1 = []
newlength_1 = []
time_1 = []
for i in xrange(runs):
    GATESFILE = open('txtfiles/print2.txt', 'r')
    NETLISTS = open('txtfiles/netlist4.txt', 'r')
    total_runs, total_length, new_length, time = run_algorithm(17, 18, 8, more_specific)
    runs_1.append(total_runs)
    length_1.append(total_length)
    newlength_1.append(new_length)
    time_1.append(time.total_seconds())
    print i

print 'MORE SPECIFIC, netlist4:'
print 'runs', runs_1
print 'length', length_1
print 'newlength', newlength_1
print 'time', time_1
