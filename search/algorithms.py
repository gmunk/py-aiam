import heapq
from collections import deque

from problem.node import Node


def best_first_search(problem):
    """Best-first search implementation.

    It assumes that the desired behaviour is that of Dijkstra's algorithm (Uniform-cost search).

    The implementation relies on the heapq module for its priority queue needs.

    Parameters
    ----------
    problem : problem.problem.Problem
        The problem which the algorithm searches.

    Returns
    -------
    problem.node.Node
        The goal node, if the function finds a solution, else None.
    """
    node = Node(state=problem.initial_state)

    reached = {node.state: node}
    frontier = []

    heapq.heappush(frontier, (node.path_cost, node))

    while frontier:
        n = heapq.heappop(frontier)[1]

        if problem.is_goal(n.state):
            return n
        for e in n.expand(problem):
            if e.state not in reached or e.path_cost < reached[e.state].path_cost:
                reached[e.state] = e
                heapq.heappush(frontier, (e.path_cost, e))

    return None


def breadth_first_search(problem):
    """Breadth-first search implementation.

    The implementation relies on the dequeue data structure for its FIFO queue needs.
    Notice that the goal checking happens immediately after the while loop reaches a node,
    in contrast best-first search performs a late goal test, after a node is popped from its
    priority queue.

    Parameters
    ----------
    problem : problem.problem.Problem
        The problem which this implementation searches.

    Returns
    -------
    problem.node.Node
        The goal node, if the function finds a solution, else None.
    """
    node = Node(state=problem.initial_state)

    if problem.is_goal(node.state):
        return node

    frontier = deque([node])
    reached = {node.state}

    while frontier:
        n = frontier.popleft()

        for e in n.expand(problem):
            if problem.is_goal(e.state):
                return e
            if e.state not in reached:
                reached.add(e.state)
                frontier.append(e)

    return None
