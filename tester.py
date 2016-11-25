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

    def makeNet(self):
        """
        make self.netline from start, end, and path, with (x, y, x) values
        :return: nothing
        """
        self.netline.append((self.start.x, self.start.y, 0))
        for point in self.path:
            self.netline.append(point)
        self.netline.append((self.end.x, self.end.y, 0))

        print self.netline

# create Chip function
class Chip(object):
    def __init__(self, width, height, GATESFILE, NETLISTS):
        '''
        :param layer: Layer object
        :param GATESFILE: file containing all gates
        '''
        self.width = width
        self.height = height
        self.gatesfile = [[int(n) for n in line.replace('\n', '').split(',')] for line in GATESFILE.readlines()]
        self.gates = [Gate((x, y)) for x, y in self.gatesfile]
        self.layers = [Layer(self.width, self.height) for i in range(7)]
        self.netlist = [[int(n) for n in line.split(',')] for line in NETLISTS.readlines()]
        self.nets = {}

        self._loadGates()

    def _loadGates(self):
        '''
        read gates from file and make gate objects on layer
        take gates and fill array with gate number pointing to
        :return:
        '''
        count = 0
        for x, y in self.gatesfile:
            count += 1
            self.layers[0].place(Gate((x, y)), x, y)

    def printChip(self):
        for layer in self.layers:
            print layer
    #
    # def placeNet(self):




width = 13
height = 18
chip = Chip(width, height, GATESFILE, NETLISTS)
layer = Layer(width,height)
# PRINT!
chip.printChip()
# print chip.gates[0]

# def runClasses(width, height, file):

array = [(1,2,7), (2,4,7),(2,1,3)]
start = Gate((2,3))
end = Gate((5,5))
test = Nets(chip.gates[1], chip.gates[4], array)
# print chip.layers[0]
Nets.makeNet(test)
# print chip.gates[7].coordinate
