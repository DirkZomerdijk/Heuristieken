# Fish 'n Chips     Laila Blomer, Dirk Zomerdijk, Anna Vos
#
# Heuristieken
# Case: Chips & Circuits
#
# run.py
# to run the algorithm, decide on all parameters, such as sorting and removal method.
# Also, decide on which netlist to place.

from functions import *

# sorting method
sorting_method = ['on_connections', 'on_connections_reverse', 'on_distance', 'on_distance_reverse']
# removing connections
removal_method = ['random', 'specific']
# netlist 1, 2, 3, 4, 5, or 6
netlist = 1

# chip parameters
if netlist < 3:
    chip_print = 1
    width = 13
else:
    chip_print = 2
    width = 17

height = 18
layers = 8

# text files
grid_file = open('txtfiles/print' + str(chip_print) + '.txt', 'r')
netlist_file = open('txtfiles/netlist' + str(netlist) + '.txt', 'r')

# start the algorithm
total_runs, total_length, new_length, time = run_algorithm(width=width,
                                                           height=height,
                                                           layer=layers,
                                                           grid_file=grid_file,
                                                           netlist_file=netlist_file,
                                                           no_path=removal_method[0],
                                                           sorting=sorting_method[2],
                                                           visualize=True)
