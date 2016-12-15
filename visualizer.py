# Heuristieken
# Chips & Circuits
#
# visualizer.py

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
from random import randint

colors =['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

class Visualizer(object):
    def __init__(self, chip):
        self.chip = chip

    def start(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim3d(0, self.chip.width - 1)
        ax.set_ylim3d(0, self.chip.height - 1)
        ax.set_zlim3d(0, self.chip.layer - 1)
        ax.set_xticks(range(self.chip.width))
        ax.set_yticks(range(self.chip.height))
        ax.set_zticks(range(self.chip.layer))
        ax.set_xlabel('Width')
        ax.set_ylabel('Heigth')
        ax.set_zlabel('Layers')
        self.addGates(ax)
        self.addNets(ax)
        plt.show()

    def addGates(self, ax):
        x = []
        y = []
        z = []
        for gate in self.chip.gates:
            z.append(0)
            x.append(gate.x)
            y.append(gate.y)

        # t = np.arange(50)
        ax.scatter(x, y, z, c='r', marker='o')

    def addNets(self, ax):
        counter = 0
        for net in self.chip.nets:
            x = []
            y = []
            z = []
            for a, b, c in net.netline:
                x.append(a)
                y.append(b)
                z.append(c)
            ax.plot_wireframe(x, y, z, color=colors[counter%8])
            counter += 1

