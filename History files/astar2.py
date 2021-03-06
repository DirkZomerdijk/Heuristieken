# A* algorithm

from chip import *
import math

class Node:
    def __init__(self, value, coordinate):
        self.value = value
        self.coordinate = coordinate
        self.parent = None
        self.G = 0
        self.H = 0

    def __str__(self):
        return '[..]'


def nextToGates(chip):
    '''
    :param chip: Chip object
    :return: returns coordinates of all children from all gates on the chip
    '''
    next = []
    for gate in chip.gates:
        for x in makeChildren2(gate, chip, gate):
            next.append(x)
    return next


def makeChildren2(node, chip, end):
    x, y, z = node.coordinate
    children = []

    options = [[x - 1, y, z], [x + 1, y, z], [x, y - 1, z], [x, y + 1, z], [x, y, z - 1], [x, y, z + 1]]
    parameters = [chip.width, chip.height, chip.layer]

    for i in range(6):
        j = int(math.floor(i / 2))
        if options[i][j] in range(parameters[j]) and (chip.layers[options[i][2]].grid[options[i][0],
                options[i][1]] == 'free' or options[i] == end.coordinate):
            children.append(options[i])

    return children


def manhattan(node, end):
    return abs(node.coordinate[0] - end.coordinate[0]) + abs(node.coordinate[1] - end.coordinate[1]) \
           + abs(node.coordinate[2] - end.coordinate[2])


def astar2(chip, start, end):
    '''

    :param chip: chip object
    :param start: Gate object
    :param end: Gate object
    :return:
    '''
    start.G = 0
    start.H = 0
    start.parent = None
    current = start

    # get array with all coordinates next to a gate
    gates_surrounding = nextToGates(chip)

    openset = set()
    closedset = set()

    openset.add(current)

    # check 'free' places
    free = 0
    for x in range(chip.width):
        for y in range(chip.height):
            for z in range(chip.layer):
                if chip.layers[z].grid[x, y] == 'free':
                    free += 1

    while openset:
        # find Node with lowest g score
        current = min(openset, key=lambda x: x.G + x.H)

        # check if we found our end gate
        if current.coordinate == end.coordinate:
            # print 'path found'
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1], None

        openset.remove(current)
        closedset.add(current)

        for node in makeChildren2(current, chip, end):
            node = Node('[--]', node)

            # If it is already in the closed set, skip it
            for child in closedset:
                if child.coordinate == node.coordinate:
                    # print 'node in closedset'
                    break

            else:
                # Otherwise if it is already in the open set
                for child in openset:
                    if child.coordinate == node.coordinate:
                        # print 'node in openset'

                        # Check if we beat the G score
                        new_g = current.G + 1

                        if node.G > new_g:
                            # If so, update the node to have a new parent
                            node.G = new_g
                            node.parent = current
                        break

                else:
                    # If it isn't in the open set, calculate the H and G score for the node
                    node.H = manhattan(node, end)
                    node.G = current.G + 1

                    # check if node is next to a gate
                    for gate in gates_surrounding:
                        if gate == node.coordinate:
                            node.G += 3

                    # Set the parent to our current item
                    node.parent = current

                    # Add it to the set
                    openset.add(node)
                    # print 'openset: ', len(openset)

                    # print closedset


        if len(openset) > free/5:
            return 'switch gates', None

    print 'closedset: ', len(closedset)
    # Throw an exception if there is no path
    return 'no path found', closedset
