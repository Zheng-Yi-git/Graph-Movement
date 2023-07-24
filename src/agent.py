from env_setup import Graph, Target
import numpy as np


# the template for agents
class Agent:
    def __init__(self, graph: Graph) -> None:
        self.location = np.random.randint(0, 40)
        self.graph = graph
        self.neighbors = [
            x - 1 for x in self.graph.node_list[self.location].neighbor_list
        ]

    def move(self):
        pass

    def examine(self):
        pass


class Agent0(Agent):
    def __init__(self, graph: Graph, target: Target) -> None:
        super().__init__(graph)
        self.target = target


class Agent1(Agent):
    def __init__(self, graph: Graph, target: Target) -> None:
        super().__init__(graph)
        self.target = target

    def _find_shortest_path(self):
        # use BFS to get the shortest path from current location to target, then return the next location
        visited = [False] * 40
        queue = []
        queue.append((self.location, []))  # (node, path)
        visited[self.location] = True
        while queue:
            s, path = queue.pop(0)
            path.append(s)

            if s == self.target.location:
                return path[1] if len(path) > 1 else path[0]

            for i in self.graph.node_list[s].neighbor_list:
                index = i - 1

                if visited[index] == False:
                    queue.append((index, path + [index]))
                    visited[index] = True

        return -1

    def move(self):
        next_location = self._find_shortest_path()
        self.location = next_location
        self.neighbors = [
            x - 1 for x in self.graph.node_list[self.location].neighbor_list
        ]


class Agent2(Agent):
    """
    A possible strategy for agent 2: always take the path with smallest expected distance to the target's next location
    """

    def __init__(self, graph: Graph, target: Target) -> None:
        super().__init__(graph)
        self.target = target

    def _BFS(self, curr_location, target_location):
        """
        return the length of the shortest path from curr_location to target_location and the number of shortest paths
        """
        visited = [False] * 40
        queue = []
        queue.append((curr_location, []))
        visited[curr_location] = True

        shortest_paths = []
        while queue:
            s, path = queue.pop(0)
            path.append(s)

            if s == target_location and (
                len(shortest_paths) == 0 or len(path) == len(shortest_paths[0])
            ):
                shortest_paths.append(path)

            for i in self.graph.node_list[s].neighbor_list:
                index = i - 1

                if visited[index] == False:
                    queue.append((index, path + [index]))
                    visited[index] = True

        if len(shortest_paths) == 0:
            return 1, 1
        else:
            return len(shortest_paths[0]) - 1, len(shortest_paths)

    def _get_path(self):
        """
        find the shortest expected distance from agent's next location to target's next location, return the next location
        """
        expected_distances: dict = {}
        for next_location in self.neighbors + [self.location]:
            expected_distances[next_location] = 0  # expected_distance
            num_shortest_paths = 0
            total_shortest_path_length = 0
            for target_location in self.target.neighbors:
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

    def move(self):
        next_location = self._get_path()
        self.location = next_location
        self.neighbors = [
            x - 1 for x in self.graph.node_list[self.location].neighbor_list
        ]


class Agent3(Agent):
    def __init__(self, graph: Graph, *args, **kwargs) -> None:
        super().__init__(graph)

    def examine(self):
        return self.location

    def move(self):
        self.location = self.examine()


class Agent4(Agent):
    def __init__(self, graph: Graph, *args, **kwargs) -> None:
        super().__init__(graph)
