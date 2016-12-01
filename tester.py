# Creates matrix with plotted net points

from visualizer import *
from search import *
from astar import *

GATESFILE = open('gates.txt', 'r')
NETLISTS = open('txtfiles/netlist1.txt', 'r')

class Layer(object):
    def __init__(self, width, height, layer_num):
        self.width = width
        self.height = height
        self.layer_num = layer_num
        self.grid = {}
        for x in range(0, width):
            for y in range(0, height):
                self.grid[x, y] = 'free'

    def place(self, item, x, y):
        self.grid[x, y] = item

    def remove(self, x, y):
        self.grid[x, y] = 'free'

    def __str__(self):
        string = ''
        for i in range(self.width):
            for j in range(self.height):
               string += str(self.grid[i, j]) + ' '
            string += '\n'
        return string

# class gate
class Gate(object):
    def __init__(self, coordinate):
        """
        layer = layer object, met z = 0
        coordinate = (x,y)
        """
        self.coordinate = [coordinate[0], coordinate[1], 0]
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.z = 0
        self.connections = []
        self.value = '[  ]'

    def addConnection(self, connection):
        self.connections.append(connection)

    def __str__(self):
        return self.value

class Nets(object):
    def __init__(self, start, end, path):
        """
        :param start: Gate object
        :param end: Gate object
        :param path: array (or dict?) with coordinates of the path of the net (x, y, z values!)
        netline: dictionary with whole net path
        """
        self.start = start
        self.end = end
        self.path = path
        self.netline = []
        self.value = '[--]'

        self.makeNet()

    def makeNet(self):
        """
        make self.netline from start, end, and path, with (x, y, x) values
        :return: nothing
        """
        self.netline.append((self.start.x, self.start.y, 0))
        for point in self.path:
            self.netline.append(point)
        self.netline.append((self.end.x, self.end.y, 0))


    def __str__(self):
        return self.value

# create Chip function
class Chip(object):
    def __init__(self, width, height, layer, GATESFILE, NETLISTS):
        '''
        :param layer: Layer object
        :param GATESFILE: file containing all gates
        '''
        self.width = width
        self.height = height
        self.layer = layer
        self._gatesfile = [[int(n) for n in line.replace('\n', '').split(',')] for line in GATESFILE.readlines()]
        self.gates = [Gate((x, y)) for x, y in self._gatesfile]
        self.layers = [Layer(self.width, self.height, i) for i in range(self.layer)]
        self.netlist = [[int(n) for n in line.split(',')] for line in NETLISTS.readlines()]
        self.nets = []

        self._loadGates()

    def _loadGates(self):
        '''
        read gates from file and make gate objects on layer
        take gates and fill array with gate number pointing to
        :return:
        '''
        count = 0
        for x, y in self._gatesfile:
            count += 1
            self.layers[0].place(Gate((x, y)), x, y)

    def placeNet(self, start, end, path):
        '''
        places a net on layer objects
        net: is an array with coordinates
        :return:
        '''

        net_pointer = Nets(start, end, path)
        for x, y, z in path:
            self.layers[z].place(net_pointer, x, y)
        self.nets.append(net_pointer)

    def removeNet(self, pointer):
        '''

        :param pointer: a pointer to a Nets object to be removed
        :return: nothing
        '''

        for x, y, z in pointer.path:
            self.layers[z].place('free', x, y)

        for i in range(len(self.nets)):
            if self.nets[i] == pointer:
                self.nets.pop(i)
        # should be even easier, with pointer.removeNet()

    def printChip(self):
        for layer in self.layers:
            print layer


def Runsearch(width, height, layer):
    chip = Chip(width, height, layer, GATESFILE, NETLISTS)

    for start, end in chip.netlist:
        Search(chip, chip.gates[start], chip.gates[end])

    # array = [(1, 1, 1), (1, 2, 1), (1, 3, 1), (1, 3, 2), (1, 4, 2), (1, 4, 1), (1, 5, 1), (1, 5, 0)]
    # chip.placeNet(chip.gates[0], chip.gates[1], array)

    Visualizer(chip).start()

def Runastar(width, height, layer):
    chip = Chip(width, height, layer, GATESFILE, NETLISTS)

    # search path
    for start, end in chip.netlist:
        path = astar(chip, chip.gates[start], chip.gates[end])
        net = []
        for node in path:
            net.append(node.coordinate)
        chip.placeNet(chip.gates[start], chip.gates[end], net)
        Visualizer(chip).start()

    print 'Finished'

# Runsearch(13, 18, 7)
Runastar(13, 18, 7)
