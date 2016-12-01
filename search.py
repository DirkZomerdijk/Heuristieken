# Minor Programmeren
#
# Fish 'n Chips
# Name: Laila Blomer - 10563865
#       Anna Vos - 10343377
#       Dirk Zomerdijk -
#
# search algoritm

import math
import random



def Search(chip, start, end):
    '''

    :param chip: chip object
    :param start: Gate object
    :param end: Gate object
    :return:
    '''
    start_coordinate = [start.x, start.y, 0]
    end_coordinate = [end.x, end.y, 0]
    layer = chip.layers[0]
    current = start_coordinate
    path = []

    while end_coordinate != current:

        if current[0] > end_coordinate[0]:
            current[0] -= 1
        elif current[0] < end_coordinate[0]:
            current[0] += 1
        elif current[1] > end_coordinate[1]:
            current[1] -= 1
        elif current[1] < end_coordinate[1]:
            current[1] += 1

        path.append((current[0], current[1], current[2]))
    chip.placeNet(start, end, path[:-1])