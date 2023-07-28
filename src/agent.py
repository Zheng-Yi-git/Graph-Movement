# -*- coding: utf-8 -*-
from env_setup import Graph


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
