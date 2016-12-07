# Creates matrix with plotted net points

from astar import *
# from astar2 import *
from collections import defaultdict
import random

GATESFILE = open('txtfiles/print1.txt', 'r')
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
        self.value = 'gate'

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
        self.value = 'net'

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
        #
        # for i in range(len(self.nets)):
        #     if self.nets[i] == pointer:
        #         self.nets.pop(i)

        for net in self.nets:
            if net == pointer:
                self.nets.remove(net)
        # should be even easier, with pointer.removeNet()

    def printChip(self):
        for layer in self.layers:
            print layer


def sortNetlist(chip):
    '''
    takes chip and returns netlist sorted by distance between gates.
    :param chip: chip object
    '''
    x = defaultdict(list)
    for start, end in chip.netlist:
        length = manhattan(chip.gates[start], chip.gates[end])
        x[length].append((start, end))
    return sorted(x.values())


def sortOnConnections(chip):
    x = defaultdict(list)
    for start, end in chip.netlist:
        connections = 0
        for netcombination in chip.netlist:
            if start == netcombination[0] or start == netcombination[1]:
                connections += 1

        x[connections].append((start, end))

    return sorted(x.values(), reverse=True)

def removeRandomNets(chip, amount):
    '''
    function removes random nets from the chip.
    :param chip: Chip object
    :param amount: amount of nets to be removed
    :return: list with start and end gates to be placed (again) on the chip, and the length of the removed nets
    '''
    temp = []
    removed = []
    netlength = 0

    # get random nets and remove them from the chip
    for i in range(amount):
        # get random net
        remove = random.choice(chip.nets)
        netlength += len(remove.path)

        temp.append((remove.start, remove.end))

        # remove net
        chip.removeNet(remove)

    for start, end in temp:
        startco = 0
        endco = 0
        # get gate numbers corresponding to net start and end coordinates
        for i in range(len(chip.gates)):
            # get start gate number
            if start.coordinate == chip.gates[i].coordinate:
                startco = i

            # get end gate number
            if end.coordinate == chip.gates[i].coordinate:
                endco = i

        removed.append((startco, endco))

    return removed, netlength

