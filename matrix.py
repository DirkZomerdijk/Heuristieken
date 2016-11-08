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

    def isPositionOnGrid(self, pos):
        """
        Return True if pos is on the grid.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return (pos.x >= 0) and (pos.x <= self.width) and (pos.y >= 0) and (pos.y <= self.height)

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
        print self.gates_coordinates
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

class Nets(object):
    def __init__(self, grid):
        """
        grid = Grid object
        nets_file is a text file with arrays containing netlists.
        """
        self.grid = grid

        # read in files with net connections
        exec(open('netlists.py').read(), globals())
        # for i in range(0, NETLISTS):
        #
        # TO DO: manier om netlists in een array te zetten ipv variabele namen




# checks!
grid = Grid(25,25)
gate = Gates(grid, GATESFILE)
gate.readGates()
coordinate = Position(2, 3)
c = gate.getGate(coordinate)
p = gate.getCoordinate(5)

Nets(grid)


# gate.readGates()
#
# grid = Grid(5,5)
# Nets(grid)
# Gates.readGates()
