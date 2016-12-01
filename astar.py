# A* algorithm

# from tester import *


class Node:
    def __init__(self, value, point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0

    def move_cost(self, other):
        return 1

    def __str__(self):
        return '[..]'


def children(point, chip):
    x, y, z = point.point
    links = [chip.layers[z].grid[d] for d in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)] if chip.layers[z].grid[d]]
    links.append(chip.layers[z - 1].grid[x, y])
    links.append(chip.layers[z + 1].grid[x, y])

    # this does return gates!!!
    return [link for link in links if (link.value != '[--]')]


# function that calculates H score, or the distance between a node and the target.
def manhattan(point, point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1] - point2.point[0]) \
           + abs(point.point[2] - point2.point[0])


def astar(chip, start, end):
    '''

    :param chip: chip object
    :param start: Gate object
    :param end: Gate object
    :return:
    '''
    start_coordinate = Node(start.value, (start.x, start.y, 0))
    end_coordinate = Node(end.value, (end.x, end.y, 0))
    current = start_coordinate

    openset = set()
    closedset = set()

    openset.add(current)

    while openset:
        # find Node with lowest g + h score
        current = min(openset, key=lambda x: x.G + x.H)

        # check if we found our end gate
        if current == end_coordinate:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]

        openset.remove(current)
        closedset.add(current)

        for node in children(current, chip):
            # If it is already in the closed set, skip it
            if node in closedset:
                continue

            # Otherwise if it is already in the open set
            if node in openset:

                # Check if we beat the G score
                new_g = current.G + current.move_cost(node)

                if node.G > new_g:
                    # If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current

            else:
                # If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, end_coordinate)

                # Set the parent to our current item
                node.parent = current

                # Add it to the set
                openset.add(node)

        # Throw an exception if there is no path
        raise ValueError('No Path Found')
