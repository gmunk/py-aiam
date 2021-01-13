import heapq
from .node import Node

DEFAULT_PRIORITY = 0


def expand(problem, node):
    state = node.state

    for a in problem.actions.get(state, {}):
        frontier_state = problem.apply_action(state, a)
        cost = node.path_cost + a.cost
        yield Node(state=frontier_state, parent=node, action=a, path_cost=cost)


def best_first_search(problem):
    frontier = []
    reached = {}

    heapq.heappush(frontier, (DEFAULT_PRIORITY, Node(state=problem.initial_state, path_cost=DEFAULT_PRIORITY)))

    while frontier:
        node = heapq.heappop(frontier)[1]
        if problem.is_goal(node.state):
            return node
        for n in expand(problem, node):
            if n.state not in reached or n.path_cost < reached[n.state].path_cost:
                reached[n.state] = n
                heapq.heappush(frontier, (n.path_cost, n))
    return None
