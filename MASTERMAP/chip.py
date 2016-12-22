# Fish 'n Chips     Laila Blomer, Dirk Zomerdijk, Anna Vos
#
# Heuristieken
# Case: Chips & Circuits
#
# chip.py


from astar import *


class Layer(object):
    '''
    a Layer object represents one layer of the chip
    '''

    def __init__(self, width, height, layer_num):
        '''
        :param width: integer, width of the chip
        :param height: integer, height of the chip
        :param layer_num: integer
        '''
        self.width = width
        self.height = height
        self.layer_num = layer_num
        self.grid = {}
        for x in range(0, width):
            for y in range(0, height):
                self.grid[x, y] = 'free'

    def place(self, item, x, y):
        '''
        :param item: object of class Nets or Gate
        :param x: integer
        :param y: integer
        places a specific item, such as a net on the grid
        '''
        self.grid[x, y] = item

    def remove(self, x, y):
        '''
        :param x: integer
        :param y: integer
        resets specific coordinate on the grid to 'free'
        '''
        self.grid[x, y] = 'free'


class Gate(object):
    '''
    Gate object represents a gate on Layer 0 of the chip
    '''
    def __init__(self, coordinate):
        '''
        :param coordinate: list with x and y coordinate of the Gate
        '''
        self.coordinate = [coordinate[0], coordinate[1], 0]
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.z = 0
        self.value = 'gate'


class Nets(object):
    '''
    Nets object represents a net on the chip from one gate to another
    '''
    def __init__(self, start, end, path):
        """
        :param start: Gate object
        :param end: Gate object
        :param path: list, with coordinates of the path of the net
        """
        self.start = start
        self.end = end
        self.path = path
        self.netline = []
        self.value = 'net'

        self.make_net()

    def make_net(self):
        """
        make self.netline from start, end, and path, with (x, y, x) values
        """
        self.netline.append((self.start.x, self.start.y, 0))
        for point in self.path:
            self.netline.append(point)
        self.netline.append((self.end.x, self.end.y, 0))


class Chip(object):
    '''
    Chip object represents the whole chip, with all layers, gates and nets.
    '''
    def __init__(self, width, height, layer, gate_file, netlist_file):
        '''
        :param width: integer
        :param height: integer
        :param layer: integer
        :param gate_file: text file containing coordinates for all gates on the print
        :param netlist_file: text file containing all gates that should be connected
        '''
        self.width = width
        self.height = height
        self.layer = layer
        self._gatesfile = [[int(n) for n in line.replace('\n', '').split(',')] for line in gate_file.readlines()]
        self.gates = [Gate((x, y)) for x, y in self._gatesfile]
        self.layers = [Layer(self.width, self.height, i) for i in range(self.layer)]
        self.netlist = [[int(n) for n in line.split(',')] for line in netlist_file.readlines()]
        self.nets = []

        self._load_gates()

    def _load_gates(self):
        '''
        Read gates from file and place Gate objects on first layer of the chip
        '''
        count = 0
        for x, y in self._gatesfile:
            count += 1
            self.layers[0].place(Gate((x, y)), x, y)

    def place_net(self, start, end, path):
        '''
        :param start: Gate object
        :param end: Gate object
        :param path: list with coordinates connecting start and end
        '''
        net_pointer = Nets(start, end, path)
        for x, y, z in path:
            self.layers[z].place(net_pointer, x, y)
        self.nets.append(net_pointer)

    def remove_net(self, pointer):
        '''
        :param pointer: Nets object to be removed
        '''
        # remove net from chip
        for x, y, z in pointer.path:
            self.layers[z].place('free', x, y)

        # remove net from nets list
        for net in self.nets:
            if net == pointer:
                self.nets.remove(net)
