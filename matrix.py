# Creates matrix with plotted net points

import numpy as np
import json

GATESFILE = open('gates.txt', 'r')
NETLISTS = open('txtfiles/netlists.txt', 'r')

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
        self.crossings = {}
        for i in range(0, width):
            for j in range(0, height):
                self.crossings[i, j] = 'free'
        # print self.crossings
    #
    # def __getitem__(self, x, y):
    #     return self.crossings[x, y]

    def markCoordinateOccupied(self, pos):
        """
        Marks coordinate at position as occupied

        pos: a Position object
        """
        self.crossings[int(pos.x)][int(pos.y)] = 1
        # print self.crossings

    def markAsGate(self, pos):
        """
        Marks coordinate at position as occupied

        pos: a Position object
        """
        self.crossings[int(pos.x)][int(pos.y)] = 2
        # print self.crossings

    def markCoordinateFree(self, pos):
        """
        Marks coordinate at position as free

        pos: a Position object
        """
        self.crossings[int(pos.x)][int(pos.y)] = 0

    def isCoordinateOccupied(self, pos):
        """
        Returns whether the grid is occupied at a certain position.

        pos: a Position object.
        returns: True if pos is on the grid, False otherwise.
        """
        return self.crossings[int(pos.x)][int(pos.y)] != 0


    def isPositionOnGrid(self, pos):
        """
        Returns True if pos is on the grid.

        pos: a Position object.
        returns: True if pos is on the grid, False otherwise.
        """
        return (pos.x >= 0) and (pos.x <= self.width) and (pos.y >= 0) and (pos.y <= self.height)

    def printGrid(self):
        """
        Prints the entire grid.

        returns: nothing
        """
        print self.crossings

class Gates(object):
    def __init__(self, grid, GATESFILE):
        """
        GATESFILE holds coordinates for all gates on the grid

        grid: a Grid object
        """
        self.grid = grid
        self.gates = GATESFILE.readlines()
        self.gates_coordinates = np.empty((0,2), int)
        # print self.gates

    # read in coordinates
    def readGates(self):
        """
        Loads GATESFILE with gate coordinates separated by ','
        Marks gates on the grid as '2'

        returns: nothing
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
            self.grid.markAsGate(coordinate)

            # return self.gates_coordinates
        #@ gate self.matrix = 1
        # print self.gates_coordinates

    def getCoordinate(self, gate):
        """
        Returns position of a certain gate number.

        gate: integer for gate number
        returns: grid position object
        """
        return Position(self.gates_coordinates[gate-1][0], self.gates_coordinates[gate-1][1])

    def getGate(self, pos):
        """
        Returns the gate number of a certain position.

        pos: a Position object
        returns: gate number (integer)
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

class Nets(object):
    def __init__(self, grid, NETSFILE):
        """
        grid: a Grid object
        NETSFILE: holds coordinates for all gates on the grid
        """
        self.grid = grid
        self.open_nets = [None] * 0
        self.closed_nets = [None] * 0
        self.nets_coordinates = {}
        self.open_nets.append(NETSFILE.readlines())
        self.length = [None] * 0

    def saveNet(self, net, coordinates):
        """
        Saves net coordinates to dictionary of nets.
        Adds net to list of closed nets and removes net from list of open nets.

        net: the two gate numbers between which the net has been placed.
        coordinates: the coordinates over which the net runs (gates excluded).
        """
        for coordinate in coordinates:
            self.nets_coordinates.update({net: coordinate})

        self.closed_nets.append(net)
        self.open_nets.pop(net)

    def getNet(self, net):
        """
        Returns the coordinates over which the net runs.

        net: the two gate numbers between which the net has been placed.
        returns: array of coordinates
        """
        return self.nets_coordinates.get(net)

    def removeNet(self, net):
        """
        Removes a net by setting all its coordinates (apart from gates) on the grid to unoccupied.

        input:
        """

        net_coordinates = self.getNet(net)
        for coordinate in net_coordinates:
            Grid.markCoordinateFree(grid, coordinate)

        self.closed_nets.pop(net)
        self.open_nets.append(net)

    def netLength(self):
        """
        Returns a list of net lengths.

        input:
        returns:
        """
        return self.length


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
    # print grid.crossings
    links = [grid.crossings[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]]
    print links
    return [link for link in links if (link.value != '1') | (link.value != '2')]

# function that calculates H score, or the distance between a node and the target.
def manhattan(point, point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1] - point2.point[0])


def aStar(net, grid):
    '''

    :param net: start and goal of netlist
    :param grid: grid object
    :return:
    '''
    # get coordinates of gatenumbers
    start_pos = Gates.getCoordinate(gate, net[0])
    goal_pos = Gates.getCoordinate(gate, net[1])
    start = Node('2',(start_pos.getX(), start_pos.getY()))
    goal = Node('2',(goal_pos.getX(), goal_pos.getY()))
    # # print goal
    # Node(1, start)
    # Node(2, goal)
    # print Node.move_cost(Node(1, start), goal)

    # The open and closed sets
    openset = set()
    closedset = set()

    # Current point is the starting point
    current = start
    # print current

    # Add the starting point to the open set
    openset.add(current)
    # print openset

    # While the open set is not empty
    while openset:
        # Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda x: x.G + x.H)
        # print current.G

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
            print node
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
        Grid.markCoordinateOccupied(grid, Position(x, y))
        print x, y

# checks!
width = 13
height = 18
grid = Grid(width, height)
gate = Gates(grid, GATESFILE)
gate.readGates()
coordinate = Position(2, 3)
c = gate.getGate(coordinate)
p = gate.getCoordinate(5)

# grid.printGrid()
grid.markCoordinateOccupied(coordinate)
grid.markCoordinateOccupied(Position(1,1))
grid.printGrid()

aStar([3,4], grid)

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

# # print nets(1)[0]
# start_gate = Gates.getCoordinate(gate, nets(n)[0])  # is position object with start coordinates
# start_x, start_y = [Position.getX(start_gate), Position.getY(start_gate)]
# end_gate = Gates.getCoordinate(gate, nets(n)[1])  # position object with target coordinates
# target_x, target_y = [Position.getX(end_gate), Position.getY(end_gate)]

# print nets(n)[0]
# print start.x
# print start.y


# next_move((start_x, start_y), (target_x, target_y), grid)



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