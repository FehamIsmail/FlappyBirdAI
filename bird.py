import math
import random
import numpy


def sig_output(x):  # returns an output in I=(-1, 1)
    if x < 0:
        return 2 * (1 - 1/(1 + math.exp(x))) - 1
    else:
        return 2 * (1/(1 + math.exp(-x))) - 1


def binary_output(x):  # returns 1 or 0
    return 0 if x < 0 else 1


def compute_dot_product(a, b):
    return a @ b


def calculate_input_nodes_sig(*inputs):
    input_nodes = []
    for i in inputs:
        input_nodes.append(sig_output(i))
    return input_nodes


def calculate_input_nodes_linear(*inputs):
    input_nodes = []
    for i in inputs:
        input_nodes.append(i)
    return input_nodes


class Bird:

    def __init__(self, isBest=False):
        self.color = "blue" if isBest else "yellow"
        self.image = [f"asset/{self.color}bird-downflap.png", f"asset/{self.color}bird-midflap.png",
                      f"asset/{self.color}bird-upflap.png"]
        self.y = 512
        self.v = 0
        self.x = 200
        self.angle = 0
        self.alive = True
        self.has_jumped = False
        self.rect = None
        self.parent_genes = None
        self.genes = [[], [], []]

    def updateImage(self, isBest):
        self.color = "blue" if isBest else "yellow"
        self.image = [f"asset/{self.color}bird-downflap.png", f"asset/{self.color}bird-midflap.png",
                      f"asset/{self.color}bird-upflap.png"]

    def setY(self, y):
        self.y = y
        self.rect.y = y - self.rect.height / 2 - 10

    def setX(self, x):
        self.x = x
        self.rect.x = x - self.rect.width / 2 - 10

    def jump(self):
        self.has_jumped = True
        if self.alive:
            self.v = -900

    def create_genes(self):
        for i in range(9):
            self.create_one_gene(i, 0)
        for i in range(3):
            self.create_one_gene(i, 1)
        for i in range(4):
            self.create_one_gene(i, 2)

    def create_one_gene(self, i, j):
        if self.parent_genes is None:
            self.genes[j].append(random.uniform(-1, 1))
        else:
            if random.random() < 0.9:
                self.genes[j].append(self.parent_genes[j][i])
            # elif random.random() < 0.5:
                # lower = self.parent_genes[j][i] - 0.6 if self.parent_genes[j][i] - 0.6 >= 0 else 0
                # upper = self.parent_genes[j][i] + 0.6 if self.parent_genes[j][i] + 0.6 <= 1 else 1
                # self.genes[j].append(random.uniform(lower, upper))
            else:
                self.genes[j].append(random.uniform(-1, 1))

    def calculate_jump(self, distance_to_bottom_pipe, distance_to_top_pipe):
        input_nodes = calculate_input_nodes_linear(self.y, distance_to_bottom_pipe, distance_to_top_pipe)
        hidden_nodes = []
        for i in range(3):
            upper = (i+1)*3
            hidden_nodes.append(sig_output(numpy.dot(input_nodes, self.genes[0][i*3:upper])) + self.genes[2][i])
        output = binary_output(numpy.dot(hidden_nodes, self.genes[1]) + self.genes[2][3])
        return True if output == 1 else False

    def getAngle(self):
        return -self.v / 30
