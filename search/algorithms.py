import heapq
from collections import deque
from .problem import Node


def expand(problem, node):
    """Expands the nodes that are connected to the one supplied as an argument.

    The function calculates the path cost from the root to each node it expands.
    It expects that the actions are represented as instances of the Action dataclass.

    Parameters
    ----------
    problem : Problem
        The problem from which this function expands nodes.
    node : Node
        The node which descendants this function is going to expand.

    Yields
    ------
    Node
        A direct descendant of the node supplied as an argument.
    """
    state = node.state

    for a in problem.actions.get(state, {}):
        frontier_state = problem.apply_action(a)
        cost = node.path_cost + a.cost
        yield Node(state=frontier_state, parent=node, action=a, path_cost=cost)


def best_first_search(problem):
    """Best-first search implementation which assumes that the desired behaviour is inline with Dijkstra's algorithm.

    The implementation relies on the heapq module for its need of a priority queue.

    Parameters
    ----------
    problem : Problem
        The problem which this implementation searches.

    Returns
    -------
    Node
        The goal node, if the function finds a solution, else None.
    """
    node = Node(state=problem.initial_state)

    reached = {node.state: node}
    frontier = []

    heapq.heappush(frontier, (node.path_cost, node))

    while frontier:
        node = heapq.heappop(frontier)[1]

        if problem.is_goal(node):
            return node
        for n in expand(problem, node):
            if n.state not in reached or n.path_cost < reached[n.state].path_cost:
                reached[n.state] = n
                heapq.heappush(frontier, (n.path_cost, n))

    return None


def breadth_first_search(problem):
    """Breadth-first search implementation.

    The implementation relies on the dequeue data structure for its need of a FIFO queue.
    Notice that the goal checking happens immediately after the while loop reaches a node.

    Parameters
    ----------
    problem : Problem
        The problem which this implementation searches.

    Returns
    -------
    Node
        The goal node, if the function finds a solution, else None.
    """
    node = Node(state=problem.initial_state)

    if problem.is_goal(node):
        return node

    frontier = deque([node])
    reached = {node.state}

    while frontier:
        node = frontier.popleft()

        for n in expand(problem, node):
            if problem.is_goal(n):
                return n
            if n.state not in reached:
                reached.add(n.state)
                frontier.append(n)

    return None


def depth_first_search(problem):
    """Depth-first search implementation.

    The implementation relies on the dequeue data structure for its need of a LIFO queue.

    Parameters
    ----------
    problem : Problem
        The problem which this implementation searches.

    Returns
    -------
    Node
        The goal node, if the function finds a solution, else None.
    """
    frontier = deque([Node(state=problem.initial_state)])

    while frontier:
        node = frontier.pop()

        if problem.is_goal(node):
            return node

        for n in expand(problem, node):
            frontier.append(n)

    return None
