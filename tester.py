# Creates matrix with plotted net points

GATESFILE = open('gates.txt', 'r')
NETLISTS = open('txtfiles/netlist1.txt', 'r')

class Layer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._grid = {}
        for x in range(0, width):
            for y in range(0, height):
                self._grid[x, y] = 'free'
    
    def place(self, item, x, y):
        self._grid[x, y] = item

    def __str__(self):
        string = ''
        for i in range(self.width):
            for j in range(self.height):
               string += str(self._grid[i, j]) + ' '
            string += '\n'
        return string

# class gate
class Gate(object):
    def __init__(self, coordinate):
        """
        layer = layer object, met z = 0
        coordinate = (x,y)
        """
        self.coordinate = coordinate
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.connections = []
        self.value = '[  ]'

    def addConnection(self, connection):
        self.connections.append(connection)

    def __str__(self):
        return self.value
#
# class Nets(object):
#     def __init__(self):



# create Chip function
class Chip(object):
    def __init__(self, width, height, GATESFILE, NETLISTS):
        '''
        :param layer: Layer object
        :param GATESFILE: file containing all gates
        '''
        self.width = width
        self.height = height
        self.gates = [[int(n) for n in line.replace('\n', '').split(',')] for line in GATESFILE.readlines()]
        self.layers = [Layer(self.width, self.height) for i in range(7)]
        self.netlist = [[int(n) for n in line.split(',')] for line in NETLISTS.readlines()]
        self.nets = {}

        self._loadGates()

    def _loadGates(self):
        '''
        read gates from file and make gate objects on layer
        :return:
        '''
        for x, y in self.gates:
            self.layers[0].place(Gate([x, y]), x, y)

    def printChip(self):
        for layer in self.layers:
            print layer
    #
    # def placeNet(self):




width = 13
height = 18
Chip = Chip(width, height, GATESFILE, NETLISTS)
layer = Layer(width,height)

# PRINT!
# Chip.printChip()

# def runClasses(width, height, file):











