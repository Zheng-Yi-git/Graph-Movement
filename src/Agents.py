from env_setup import Graph, Target
import numpy as np

# the template for agents
class Agent:
    def __init__(self, graph: Graph) -> None:
        self.location = np.random.randint(0, 40)
        self.graph = graph
        self.neighbors = graph.node_list[self.location].neighbor_list

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
        queue.append((self.location, [])) # (node, path)
        visited[self.location] = True
        while queue:
            s, path = queue.pop(0)
            path.append(s)

            if s == self.target.location:
                return path[1]
            
            for i in self.graph.node_list[s].neighbor_list:
                index = i - 1
                
                if visited[index] == False:
                    queue.append((index, path + [index]))
                    visited[index] = True

        return -1
    
    def move(self):
        next_location = self._find_shortest_path()
        self.location = next_location
        self.neighbors = self.graph.node_list[self.location].neighbor_list

