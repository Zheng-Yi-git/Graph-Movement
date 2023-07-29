# -*- coding: utf-8 -*-
from env_setup import Graph
from functools import lru_cache
import numpy as np


class GraphAgent0(Graph):
    def __init__(self):
        super().__init__()

    def move_agent(self):
        pass


class GraphAgent1(Graph):
    def __init__(self):
        super().__init__()

    def _find_shortest_path(self):
        # use BFS to get the shortest path from current location to target, then return the next location
        visited = [False] * self.node_num
        queue = []
        queue.append((self.agent_name, []))  # (node name, path using node name)
        visited[self.name_id_dict[self.agent_name]] = True

        while queue:
            s, path = queue.pop(0)
            path.append(s)
            if s == self.target_name:
                return path[1] if len(path) > 1 else path[0]
            for i in self.node_list[self.name_id_dict[s]].neighbor_list:
                if not visited[self.name_id_dict[i]]:
                    queue.append((i, path + [i]))
                    visited[self.name_id_dict[i]] = True
        return -1

    def move_agent(self):
        self.node_list[self.name_id_dict[self.agent_name]].status = 0
        self.agent_name = self._find_shortest_path()
        self.node_list[self.name_id_dict[self.agent_name]].status = 1


class GraphAgent2(Graph):
    def __init__(self):
        super().__init__()

    def _BFS(self, agent_name, target_name):
        """
        return the length of the shortest path from curr_location to target_location and the number of shortest paths
        """
        visited = [False] * 40
        queue = []
        queue.append((agent_name, []))
        visited[self.name_id_dict[agent_name]] = True
        shortest_paths = []

        while queue:
            s, path = queue.pop(0)
            path.append(s)
            if s == target_name and (
                len(shortest_paths) == 0 or len(path) == len(shortest_paths[0])
            ):
                shortest_paths.append(path)
            for i in self.node_list[self.name_id_dict[s]].neighbor_list:
                if not visited[self.name_id_dict[i]]:
                    queue.append((i, path + [i]))
                    visited[self.name_id_dict[i]] = True
        if len(shortest_paths) == 0:
            return 1, 1
        else:
            return len(shortest_paths[0]) - 1, len(shortest_paths)

    def _get_path(self):
        """
        find the shortest expected distance from agent's next location to target's next location, return the next location
        """
        expected_distances: dict = {}

        for next_location in self.node_list[
            self.name_id_dict[self.agent_name]
        ].neighbor_list + [self.agent_name]:
            expected_distances[next_location] = 0  # expected_distance
            num_shortest_paths = 0
            total_shortest_path_length = 0

            for target_location in self.node_list[
                self.name_id_dict[self.target_name]
            ].neighbor_list:
                shortest_path_length, num_shortest_paths = self._BFS(
                    next_location, target_location
                )
                total_shortest_path_length += shortest_path_length * num_shortest_paths
                num_shortest_paths += num_shortest_paths

            expected_distances[next_location] = (
                total_shortest_path_length / num_shortest_paths
            )

        # find the next location with smallest expected distance
        return min(expected_distances, key=expected_distances.get)

    def move_agent(self):
        self.node_list[self.name_id_dict[self.agent_name]].status = 0
        self.agent_name = self._get_path()
        self.node_list[self.name_id_dict[self.agent_name]].status = 1


class GraphAgent4(Graph):
    def __init__(self):
        super().__init__()
    
    def initialize(self, random_seed=0):
        super().initialize(random_seed)
        # initialize the belief of each node to be equal and sum to 1
        for node in self.node_list:
            node.belief = 1 / self.node_num
        self.agent_history = []  # record the agent's location history
        self.agent_history.append(self.agent_name)
    

    @lru_cache(maxsize=1000)
    def filter(self, agent_event, target_name):
        if agent_event == 0:
            return 1 / self.node_num
        else:
            if self.agent_history[agent_event] == target_name:
                return 0
            numerator = 0
            for neighbor in self.node_list[
                self.name_id_dict[target_name]
            ].neighbor_list:
                # print((
                #     self.filter(agent_event - 1, neighbor)
                # ))
                numerator += 1 / (self.node_list[self.name_id_dict[neighbor]].degree) * (
                    self.filter(agent_event - 1, neighbor)
                )

            denominator = self.prediction(
                agent_event - 1,
                self.node_list[self.name_id_dict[self.agent_history[agent_event]]].name,
            )
            return numerator / (denominator * 39)

    @lru_cache(maxsize=1000)
    def prediction(self, agent_event, target_name):
        if agent_event == 0:
            return 1 / self.node_num
        belief = 0
        for neighbor in self.node_list[self.name_id_dict[target_name]].neighbor_list:
            belief += self.filter(agent_event, neighbor) * 1 / self.node_list[
                self.name_id_dict[neighbor]
            ].degree

        return belief

    def move_agent(self):
        self.node_list[self.name_id_dict[self.agent_name]].status = 0
        for node in self.node_list:
            node.belief = self.prediction(len(self.agent_history) - 1, node.name)
            # print(node.name, node.belief)

        # # print the sum of belief
        # sum_belief = 0
        # for node in self.node_list:
        #     sum_belief += node.belief
        # print(sum_belief)
        # # 统计最大的belief的node数量
        # max_belief = max(self.node_list, key=lambda x: x.belief).belief
        # max_belief_num = 0
        # for node in self.node_list:
        #     if node.belief == max_belief:
        #         max_belief_num += 1
        # print(max_belief_num)
        self.agent_name = max(self.node_list, key=lambda x: x.belief).name
        self.agent_history.append(self.agent_name)
        self.node_list[self.name_id_dict[self.agent_name]].status = 1
