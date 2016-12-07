# A* algorithm

# from chip import *
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


def makeChildren(node, chip, end):
    x, y, z = node.coordinate
    children = []

    options = [[x - 1, y, z], [x + 1, y, z], [x, y - 1, z], [x, y + 1, z], [x, y, z - 1], [x, y, z + 1]]
    parameters = [chip.width, chip.height, chip.layer]

    for i in range(6):
        j = int(math.floor(i / 2))
        if options[i][j] in range(parameters[j]) and (chip.layers[options[i][2]].grid[options[i][0],
                options[i][1]] == 'free' or options[i] == end.coordinate):
            children.append(Node('[--]', options[i]))

    return children


def manhattan(node, end):
    return abs(node.coordinate[0] - end.coordinate[0]) + abs(node.coordinate[1] - end.coordinate[1]) \
           + abs(node.coordinate[2] - end.coordinate[2])


def astar(chip, start, end):
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
    print end.coordinate

    openset = set()
    closedset = set()

    openset.add(current)

    while openset:
        # find Node with lowest g score
        current = min(openset, key=lambda x: x.G + x.H)

        # check if we found our end gate
        if current.coordinate == end.coordinate:
            print 'path found'
            path = []
            while current.parent != start:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]

        openset.remove(current)
        closedset.add(current)

        for node in makeChildren(current, chip, end):
            # If it is already in the closed set, skip it
            if node in closedset:
                continue

            # Otherwise if it is already in the open set
            if node in openset:
                print 'node in openset'

                # Check if we beat the G score
                new_g = current.G + 1

                if node.G > new_g:
                    # If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current

            else:
                # If it isn't in the open set, calculate the H and G score for the node
                node.H = manhattan(node, end)
                node.G = current.G + 1

                # Set the parent to our current item
                node.parent = current

                # Add it to the set
                openset.add(node)

    # Throw an exception if there is no path
    raise ValueError('No Path Found')
