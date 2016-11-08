# Creates matrix with plotted net points

import numpy as np
import json

GATESFILE = open('gates.txt', 'r')
NETLISTS = 0

class Position(object):
    def __init__(self, x, y):
        # self.grid = grid
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.crossings = np.zeros(shape=(width, height))
        # print self.crossings

    def markCrossingOccupied(self, pos):
        """
        Marks crossing at position as occupied

        pos: a Position object
        """
        self.crossings[int(pos.x)][int(pos.y)] = 1
        # print self.crossings

    def isPositionOnGrid(self, pos):
        """
        Return True if pos is on the grid.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return (pos.x >= 0) and (pos.x <= self.width) and (pos.y >= 0) and (pos.y <= self.height)

    def printGrid(self):
        print self.crossings

class Gates(object):
    def __init__(self, grid, GATESFILE):
        """
        GATESFILE holds coordinates for all gates on the grid
        grid = a Grid object
        """
        self.grid = grid
        self.gates = GATESFILE.readlines()
        self.gates_coordinates = np.empty((0,2), int)
        # print self.gates

    # read in coordinates
    def readGates(self):
        """
        Loads GATESFILE with gate coordinates separated by ','
        Marks gates on the grid as '1'

        Return nothing (right??)
        """
        # iterate over lines
        lines = 0
        for line in self.gates:
            # print line
            lines += 1
            self.x, self.y = line.split(',')
            # print self.x
            # print self.y
            newrow = [int(self.x), int(self.y)]

            # append new coordinate to array
            self.gates_coordinates = np.vstack([self.gates_coordinates, newrow])

            # mark gates as occupied
            coordinate = Position(self.x, self.y)
            self.grid.markCrossingOccupied(coordinate)

            # return self.gates_coordinates
        #@ gate self.matrix = 1
        # print self.gates_coordinates
    #def connections
    def getCoordinate(self, gate):
        """
        takes integer for gate number, and returns grid position object
        """
        return Position(self.gates_coordinates[gate-1][0], self.gates_coordinates[gate-1][1])

    def getGate(self, pos):
        """
        takes position object, and returns gate value (integer)
        """
        # print self.gates_coordinates
        gate_value = 1
        for line in self.gates_coordinates:
            # print line
            if line[0] == pos.x and line[1] == pos.y:
                # print gate_value
                return gate_value
            else:
                gate_value += 1
        return False

    #def complete

def nets(n):
    """
    function that returns gates, and takes integer n to determine array index
    """
    # read in files with net connections
    exec (open('netlists.py').read(), globals())
    return netlist_1[n]





# SEARCH ALGORITHM

class Node:
    def __init__(self, value, point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0

    def move_cost(self, other):
        return 0 if self.value == '.' else 1


def children(point, grid):
    x, y = point.point
    links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]]
    return [link for link in links if link.value != '%']

# function that calculates H score, or the distance between a node and the target.
def manhattan(point, point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1] - point2.point[0])


def aStar(start, goal, grid):
    # The open and closed sets
    openset = set()
    closedset = set()
    # Current point is the starting point
    current = start
    # Add the starting point to the open set
    openset.add(current)
    # While the open set is not empty
    while openset:
        # Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o: o.G + o.H)
        # If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        # Remove the item from the open set
        openset.remove(current)
        # Add it to the closed set
        closedset.add(current)
        # Loop through the node's children/siblings
        for node in children(current, grid):
            # If it is already in the closed set, skip it
            if node in closedset:
                continue
            # Otherwise if it is already in the open set
            if node in openset:
                # Check if we beat the G score
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    # If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                # If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                # Set the parent to our current item
                node.parent = current
                # Add it to the set
                openset.add(node)
    # Throw an exception if there is no path
    raise ValueError('No Path Found')


def next_move(start, target, grid):
    # Convert all the points to instances of Node
    for x in xrange(grid.width):
        for y in xrange(grid.height):
            grid[x][y] = Node(grid[x][y], (x, y))
    # Get the path
    path = aStar(grid[start[0]][start[1]], grid[target[0]][target[1]], grid)
    # Output the path
    print len(path) - 1
    for node in path:
        x, y = node.point
        Grid.markCrossingOccupied(grid, Position(x, y))
        print x, y

# checks!
grid = Grid(13, 18)
gate = Gates(grid, GATESFILE)
gate.readGates()
coordinate = Position(2, 3)
c = gate.getGate(coordinate)
p = gate.getCoordinate(5)

# print nets(1)
# print Grid.printGrid(grid)

# gate.readGates()
#
# grid = Grid(5,5)
# Nets(grid)
# Gates.readGates()

# iterate over nets
    # call next_move function for every net coordinate
n = 0

# print nets(1)[0]
start_gate = Gates.getCoordinate(gate, nets(n)[0])  # is position object with start coordinates
start_x, start_y = [Position.getX(start_gate), Position.getY(start_gate)]
end_gate = Gates.getCoordinate(gate, nets(n)[1])  # position object with target coordinates
target_x, target_y = [Position.getX(end_gate), Position.getY(end_gate)]

# print nets(n)[0]
# print start.x
# print start.y

next_move((start_x, start_y), (target_x, target_y), grid)



## EXAMPLE with pacman
# net_x, net_y = [int(i) for i in raw_input().strip().split()]
# target_x, target_y = [int(i) for i in raw_input().strip().split()]
# x, y = [int(i) for i in raw_input().strip().split()]
#
# grid = []
# for i in xrange(0, x):
#     grid.append(list(raw_input().strip()))
#
# next_move((net_x, net_y), (target_x, target_y), grid)