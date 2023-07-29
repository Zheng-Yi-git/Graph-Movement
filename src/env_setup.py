# -*- coding: utf-8 -*-
import numpy as np
from random import sample, seed
from datetime import datetime
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class Node(object):
    def __init__(self, name):
        self.name = name  # 1, 2, ..., 40, which is for displaying
        self.neighbor_list = []  # also use name to represent a node
        self.degree = 0
        self.coord = None  # (x, y) when plotted on a 2D plane
        self.status = 0  # 0: normal, 1: agent, 2: target
        self.belief = 0.01


class Graph(ABC):
    def __init__(self):
        self.node_num = 40
        self.node_list = []
        self.edge_list = []
        self.target_name = None
        self.agent_name = None
        self.name_id_dict = {
            i: (i - 1) for i in range(1, 41)
        }  # key: node name, value: node id
        # when you need to access a node, use self.node_list[self.name_id_dict[node_name]]
        self.color_dict = {0: "black", 1: "blue", 2: "red"}

    def initialize(self, random_seed=0):
        np.random.seed(random_seed)
        seed(random_seed)
        name_list = [i for i in range(1, self.node_num + 1)]
        neighbor_dict = {}  # key: node name, value: neighbor list (also use name)

        # generate default edges, i.e., 1-2, 2-3, ..., 39-40, 40-1
        for i in range(0, self.node_num):
            neighbor_dict[name_list[i]] = [
                name_list[i - 1],
                name_list[(i + 1) % self.node_num],
            ]
            self.edge_list.append((name_list[i], name_list[i - 1]))

        # generate another 10 edges
        edge_num = 0
        while edge_num < 10:
            pair = sample(name_list, 2)
            if pair[1] not in neighbor_dict[pair[0]]:
                neighbor_dict[pair[0]].append(pair[1])
                neighbor_dict[pair[1]].append(pair[0])
                self.edge_list.append(tuple(pair))
                edge_num += 1
                name_list.remove(pair[0])
                name_list.remove(pair[1])

        # initialize nodes
        for i in range(1, self.node_num + 1):
            node = Node(name=i)
            node.neighbor_list = neighbor_dict[i]
            node.degree = len(neighbor_dict[i])
            self.belief = 1 / self.node_num
            self.node_list.append(node)

        # generate coordinates for nodes, which is for plotting the graph
        center_x = 8
        center_y = 8
        radius = 7
        angles = np.linspace(-np.pi / 2, 3 * np.pi / 2, 40, endpoint=False)
        x = center_x + radius * np.cos(angles)
        y = center_y + radius * np.sin(angles)
        coord_list = list(zip(x, y))
        for node in self.node_list:
            node.coord = coord_list[self.name_id_dict[node.name]]

        # randomly select an agent and a target
        self.target_name = np.random.choice(range(1, self.node_num + 1))
        self.agent_name = np.random.choice(range(1, self.node_num + 1))
        self.node_list[self.name_id_dict[self.target_name]].status = 2
        self.node_list[self.name_id_dict[self.agent_name]].status = 1

    def plot(self, step, save_dir="../results/figs/", plot_belief=False):
        # when an agent needs to plot the belief of each node, override this method with super().plot(step, plot_belief=True)
        fig, ax = plt.subplots()
        plt.axis("equal")
        fig.set_size_inches(8, 8)
        for _, node in enumerate(self.node_list):
            ax.add_patch(
                plt.Circle(node.coord, radius=0.42, color=self.color_dict[node.status])
            )
            ax.text(
                node.coord[0],
                node.coord[1],
                "{}\n{:.2f}".format(node.name, node.belief)
                if plot_belief
                else node.name,
                ha="center",
                va="center",
                color="white",
            )
        for edge in self.edge_list:
            ax.plot(
                [
                    self.node_list[self.name_id_dict[edge[0]]].coord[0],
                    self.node_list[self.name_id_dict[edge[1]]].coord[0],
                ],
                [
                    self.node_list[self.name_id_dict[edge[0]]].coord[1],
                    self.node_list[self.name_id_dict[edge[1]]].coord[1],
                ],
                "k-",
            )
        plt.title("Step {}".format(step))
        plt.savefig(save_dir + datetime.now().strftime("%Y%m%d%H%M%S%f") + ".png")
        plt.close()

    def move_target(self):
        self.node_list[self.name_id_dict[self.target_name]].status = 0
        self.target_name = np.random.choice(
            self.node_list[self.name_id_dict[self.target_name]].neighbor_list
        )
        self.node_list[self.name_id_dict[self.target_name]].status = 2

    @abstractmethod
    def move_agent(self):
        pass

    def capture(self):
        return self.agent_name == self.target_name


class Graph1(Graph):
    def move_agent(self):
        pass


if __name__ == "__main__":
    g = Graph1()
    g.initialize()
    for node in g.node_list:
        print(node.name, node.neighbor_list, node.degree, node.coord, node.status)
    print(g.edge_list)
    g.plot(plot_belief=True)
    g.move_target()
    g.plot()
    g.move_target()
    g.plot()
