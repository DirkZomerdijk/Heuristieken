# Fish 'n Chips     Laila Blomer, Dirk Zomerdijk, Anna Vos
#
# Heuristieken
# Case: Chips & Circuits
#
# astar.py

from chip import *
import math


class Node:
    '''
    A Node represents a coordinate on the chip which is being searched by the A* algorithm
    '''
    def __init__(self, value, coordinate):
        '''
        :param value: a string, which represents the value of that node
        :param coordinate: a list with [x, y, z]
        '''
        self.value = value
        self.coordinate = coordinate
        self.parent = None
        self.G = 0
        self.H = 0

    def __str__(self):
        return '[..]'


def next_to_gates(chip):
    '''
    :param chip: Chip object
    :return: returns coordinates of all children from all gates on the chip
    '''
    next = []
    for gate in chip.gates:
        for x in make_children(gate, chip, gate):
            next.append(x)
    return next


def make_children(node, chip, end):
    '''
    :param node: Node instance
    :param chip: Chip object
    :param end: Gate object
    :return: returns surrounding coordinates of node
    '''
    # get coordinates of node
    x, y, z = node.coordinate

    child_options = [[x - 1, y, z], [x + 1, y, z], [x, y - 1, z], [x, y + 1, z], [x, y, z - 1], [x, y, z + 1]]
    parameters = [chip.width, chip.height, chip.layer]

    # check value of surrounding coordinates
    children = []
    for i in xrange(6):
        j = int(math.floor(i / 2))
        if child_options[i][j] in range(parameters[j]) and (chip.layers[child_options[i][2]].grid[child_options[i][0],
                child_options[i][1]] == 'free' or child_options[i] == end.coordinate):
            children.append(child_options[i])

    # return free coordinates
    return children


# returns the chip length between two coordinates
def manhattan(node, end):
    '''
    :param node: Node instance
    :param end: Gate object, the target gate of the net
    :return: minimum netlength from the node to the end Gate.
    '''
    return abs(node.coordinate[0] - end.coordinate[0]) + abs(node.coordinate[1] - end.coordinate[1]) \
           + abs(node.coordinate[2] - end.coordinate[2])


def astar(chip, start, end, restrictions, switch, up):
    '''
    A* algorithm looks for the shortest path between the start and end coordinate, based on the cost of a specific move
    (coordinate change) and the minimum length between that coordinate and the end coordinate.
    :param chip: chip object
    :param start: Gate object
    :param end: Gate object
    :param restrictions: is true, extra costs are added to the coordinates surrounding gates
    :param switch: if true, the start and end gate are switched and A* is runned again
    :param up: if true, coordinates on higher layers get lower cost than coordinates on lower layers
    :return: if a path is found: that is returned. if no path is found, this is also returned.
    '''
    # define cost variables
    start.G = 0
    start.H = 0

    # set parent of start node to NULL
    start.parent = None
    current = start

    # initiate lists for visited nodes to visit nodes
    openset = set()
    closedset = set()

    openset.add(current)

    # check 'free' coordinates
    free = 0
    for x in xrange(chip.width):
        for y in xrange(chip.height):
            for z in xrange(chip.layer):
                if chip.layers[z].grid[x, y] == 'free':
                    free += 1

    while openset:
        # find node with lowest g + h score
        current = min(openset, key=lambda x: x.G + x.H)

        # if end coordinate is found
        if current.coordinate == end.coordinate:
            # save path
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1], None

        openset.remove(current)
        closedset.add(current)

        # for each surrounding free coordinate
        for child in make_children(current, chip, end):
            # create new node
            child = Node('[--]', child)

            # if already in closed set, skip
            for node in closedset:
                if node.coordinate == child.coordinate:
                    break

            else:
                # else, if already in open set
                for node in openset:
                    if node.coordinate == child.coordinate:
                        # check if we beat the G score
                        new_g = current.G + 1
                        if child.G > new_g:
                            # set parent to current node
                            child.G = new_g
                            child.parent = current
                        break

                # if child not in openset or closedset
                else:
                    # calculate the H and G score for child
                    child.H = manhattan(child, end)
                    child.G = current.G + 1

                    # if child has a higher z-value decrease cost
                    if up and child.coordinate[2] > current.coordinate[2]:
                        child.G -= 1

                    # add costs to nodes surrounding gates
                    if restrictions:
                        # get array with all coordinates next to a gate
                        gates_surrounding = next_to_gates(chip)

                        # check if node is next to a gate
                        for gate in gates_surrounding:
                            if gate == child.coordinate:
                                child.G += 3

                    # set the parent to our current item
                    child.parent = current

                    # add child to openset
                    openset.add(child)

        # if observed space is larger than 1/3 of free space, switch gates
        if len(closedset) > free/2 and switch:
            return 'switch gates', None

    return 'no path found', closedset
