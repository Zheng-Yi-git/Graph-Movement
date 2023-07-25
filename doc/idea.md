# Idea for Assignment 2 (Phase 1)

## File Structure

`../src/env_setup.py` implemented the environment setup procedure for the assignment. In this file, we designed a Node class to represent the node in the graph, and we also designed a Graph class to represent the whole graph. Also, a Target class is designed to represent the target that moves in the graph.

`../src/agent.py` implemented Agent 0 through 7, which utilize different strategies to find the target.

`../src/analysis.ipynb` implemented all the experiments to examine the performance of different agents.

## Agent Implementation Idea

### Agent 0

Agent 0 uses the most naive strategy to find the target, and we just implemented as the doc described.

### Agent 1

Agent 1 always moves to reduce the distance between itself and the target. Here we implemented BFS to find the shortest path between the agent and the target.

### Agent 2

One of the possible drawbacks of Agent 1 is that it randomly chooses a direction when there are multiple shortest paths. Agent 2 tries to solve this problem by minimizing the expectation between the agent's next position and the target's next position.

### Agent 3

Agent 3 is similar to Agent 0, we just implemented it as the doc described.

### Agent 4

As the doc described, Agent 4 always examines the node with the highest probability of containing the target. We implemented this by first initializing the belief of each node to be 1 / (number of nodes), and then update the belief of each node according to the observation based on Bayes' rule. Then it just chooses the node with the highest belief, does this over and over again until it finds the target.

### Agent 5

When two nodes have the same belief, Agent 4 just chooses a node randomly. Agent 5 tries to solve this problem by considering the average belief of the neighbors of each node. To be more specific, assume Node 1 and Node 2 have the same belief, Agent 5 will calculate the average belief of Node 1's neighbors and Node 2's neighbors (denoted as avg 1 and avg 2), and then choose the node with the higher average belief.

### Agent 6

Agent 6 is the combination of Agent 1 and Agent 4. It first uses Agent 4 to update the belief of each node, and then uses Agent 1 to find the shortest path between the agent and the position with the highest belief, just assuming that the target is in that position.

### Agent 7

Inspired by Agent 2 and Agent 5, Agent 7 should also optimize the cases when there are ties. For example, combining Agent 2 and Agent 5 may be a choice. But this is just a naive idea, and we may need more time to consider the details.
