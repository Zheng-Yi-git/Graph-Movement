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
        self.neighbors = self.graph.node_list[self.location].neighbor_list


class Agent2(Agent):
    '''
    Only a possible implementation of Agent2: The key to capture the target might be to always take the shortest path. Hence, if there
    are more than 1 such paths, the agent should stay at where the shortest paths intersect.

    Note: a possible improvement is to consider the targets' possible next locations, and choose the shortest path that leads to the
    most possible next locations of the target.
    '''

    def __init__(self, graph: Graph, target: Target) -> None:
        super().__init__(graph)
        self.target = target

    def _find_shortest_path(self):
        # use BFS to find the shortest path, if there are more than 1 shortest paths, reach the intersection of them
        visited = [False] * 40
        queue = []
        queue.append((self.location, [])) # (node, path)
        visited[self.location] = True
        
        shortest_paths = []

        while queue:
            s, path = queue.pop(0)
            path.append(s)

            if s == self.target.location:
                shortest_paths.append(path[1] if len(path) > 1 else path[0])
            
            for i in self.graph.node_list[s].neighbor_list:
                index = i - 1
                
                if visited[index] == False:
                    queue.append((index, path + [index]))
                    visited[index] = True

        if len(shortest_paths) == 1:
            return shortest_paths[0][0]

        # find the intersection of the shortest paths
        path_to_intersection = shortest_paths[0]
        for path in shortest_paths[1:]:
            for node in path:
                if node in path_to_intersection:
                    path_to_intersection = path_to_intersection[:path_to_intersection.index(node) + 1]
                    break

        return path_to_intersection[0]
        


        


