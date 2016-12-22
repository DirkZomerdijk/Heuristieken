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

# chip parameters
# if print 1 is used, width should be 13. If print 2 is used width should be 17
width = [13, 17]
height = 18
layers = 8

# text files
grid = open('txtfiles/print1.txt', 'r')
# netlist 1, 2, 3 should be run with print 1. Netlist 4, 5, 6 with print 2.
netlist = open('txtfiles/netlist1.txt', 'r')

total_runs, total_length, new_length, time = run_algorithm(width=width[0],
                                                           height=height,
                                                           layer=layers,
                                                           grid_file=grid,
                                                           netlist_file=netlist,
                                                           no_path=removal_method[1],
                                                           sorting=sorting_method[2],
                                                           visualize=True)
