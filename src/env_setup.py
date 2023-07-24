# -*- coding: utf-8 -*-
import numpy as np
from random import sample


class Node(object):
    def __init__(self, id):
        self.id = id
        self.neighbor_list = []
        self.degree = 0


class Graph(object):
    def __init__(self):
        self.node_num = 40
        self.node_list = []

    def initialize(self):
        id_list = [i for i in range(1, 41)]
        neighbor_dict = {}  # id: neighbor_list
        for i in range(0, 40):
            # 1-2, 2-3, ..., 39-40, 40-1
            neighbor_dict[id_list[i]] = [id_list[i - 1], id_list[(i + 1) % 40]]
        edge_num = 0
        while edge_num < 10:
            # add another 10 edges
            pair = sample(id_list, 2)
            if pair[1] not in neighbor_dict[pair[0]]:
                neighbor_dict[pair[0]].append(pair[1])
                neighbor_dict[pair[1]].append(pair[0])
                edge_num += 1
                id_list.remove(pair[0])
                id_list.remove(pair[1])
        for i in range(1, 41):
            node = Node(i)
            node.neighbor_list = neighbor_dict[i]
            node.degree = len(neighbor_dict[i])
            self.node_list.append(node)


class Target(object):
    def __init__(self, graph: Graph, init_location: int):
        self.location = init_location
        self.neighbors = graph.node_list[self.location].neighbor_list
        self.graph = graph

    def move(self):
        self.location = np.random.choice(self.neighbors) - 1
        self.neighbors = [
            x - 1 for x in self.graph.node_list[self.location].neighbor_list
        ]


if __name__ == "__main__":
    g = Graph()
    g.initialize()
    for node in g.node_list:
        print(node.id, node.neighbor_list, node.degree)
