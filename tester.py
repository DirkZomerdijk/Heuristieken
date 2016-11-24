# Creates matrix with plotted net points

GATESFILE = open('gatestest.txt', 'r')
NETLISTS = open('txtfiles/netlists.txt', 'r')

class Grid(object):
    def __init__(self, width, height, layer):
        self.width = width
        self.height = height
        self.layer = layer
        self.chip = {}
        for x in range(0, width):
            for y in range(0, height):
                self.chip[x, y] = 'free'


# class gate
class Gate(object):
    def __init__(self, coordinate):
        """
        grid = grid object, met z = 0
        coordinate = (x,y)
        """
        self.coordinate = coordinate
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.connections = []
        self.value = 'gate'

    def addConnection(self, connection):
        self.connections.append(connection)

# create board function
class Board(object):
    def __init__(self, width, height, GATESFILE):
        '''
        :param grid: Grid object
        :param GATESFILE: file containing all gates
        '''
        self.width = width
        self.height = height
        self.gates = GATESFILE.readlines()

    def drawGrids(self):
        '''

        :return:
        '''
        for layer in range(0,7):
            Grid(self.width,self.height,layer)

    def loadGatesOnGrid(self):
        '''
        read gates from file and make gate objects on grid
        :return:
        '''
        for line in self.gates:
            x, y = line.split(',')
            Grid(self.width, self.height, 0).chip[x, y[:-1]] = Gate([x, y[:-1]])
            print Grid(self.width, self.height, 0).chip[x, y[:-1]]

    def printBoard(self):
        for x in range(0, width):
            print '\n'
            for y in range(0, height):
                print Grid(self.width, self.height, 0).chip[x, y],




width = 5
height = 5
board = Board(width, height, GATESFILE)
board.drawGrids()
board.loadGatesOnGrid()
board.printBoard()

# print board.__dict__

# def runClasses(width, height, file):











