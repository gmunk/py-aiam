import heapq
from collections import deque
from .problem import Node

DEFAULT_PATH_COST = 0


def expand(problem, node):
    state = node.state

    for a in problem.actions.get(state, {}):
        frontier_state = problem.apply_action(a)
        cost = node.path_cost + a.cost
        yield Node(state=frontier_state, parent=node, action=a, path_cost=cost)


def best_first_search(problem):
    node = Node(state=problem.initial_state, parent=None, action=None, path_cost=DEFAULT_PATH_COST)

    reached = {node.state: node}
    frontier = []

    heapq.heappush(frontier, (DEFAULT_PATH_COST, node))

    while frontier:
        node = heapq.heappop(frontier)[1]

        if problem.is_goal(node.state):
            return node
        for n in expand(problem, node):
            if n.state not in reached or n.path_cost < reached[n.state].path_cost:
                reached[n.state] = n
                heapq.heappush(frontier, (n.path_cost, n))

    return None


def breadth_first_search(problem):
    node = Node(state=problem.initial_state, parent=None, action=None, path_cost=DEFAULT_PATH_COST)

    if problem.is_goal(node.state):
        return node

    frontier = deque([node])
    reached = {node.state}

    while frontier:
        node = frontier.popleft()

        for n in expand(problem, node):
            if problem.is_goal(n.state):
                return n
            if n.state not in reached:
                reached.add(n.state)
                frontier.append(n)

    return None


def depth_first_search(problem):
    node = Node(state=problem.initial_state, parent=None, action=None, path_cost=DEFAULT_PATH_COST)

    if problem.is_goal(node.state):
        return node

    frontier = deque([node])

    while frontier:
        node = frontier.pop()

        if problem.is_goal(node.state):
            return node

        for n in expand(problem, node):
            frontier.append(n)

    return None