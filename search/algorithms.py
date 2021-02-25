import heapq
from collections import deque
from typing import Optional, Callable

from problem.node import Node, cutoff, failure
from problem.problem import Problem
from search.helpers import proceed


def best_first_search(problem: Problem) -> Optional[Node]:
    """Best-first search implementation.

    It assumes that the desired behaviour is that of Dijkstra's algorithm (Uniform-cost search).

    The implementation relies on the heapq module for its priority queue needs.

    Parameters
    ----------
    problem : problem.problem.Problem
        The problem which the algorithm searches.

    Returns
    -------
    Node
        Solution node, if the function finds one, else None.
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


def breadth_first_search(problem: Problem) -> Optional[Node]:
    """Breadth-first search implementation.

    It relies on the dequeue data structure for its FIFO queue needs.
    Notice that the goal checking happens immediately after the while loop reaches a node,
    in contrast best-first search performs a late goal test, after a node is popped from its
    priority queue.

    Parameters
    ----------
    problem : problem.problem.Problem
        The problem which this implementation searches.

    Returns
    -------
    Node
        Solution node, if the function finds one, else None.
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


def depth_first_search(problem: Problem) -> Optional[Node]:
    """Depth-first search implementation.

    It relies on the dequeue data structure for its need of a LIFO queue.

    Parameters
    ----------
    problem: problem.problem.Problem
        The problem which this implementation searches.

    Returns
    -------
    Node
        Solution node, if the function finds one, else None.
    """
    frontier = deque([Node(state=problem.initial_state)])

    while frontier:
        node = frontier.pop()

        if problem.is_goal(node.state):
            return node

        frontier.extend([n for n in node.expand(problem)])

    return None


def depth_limited_search(problem: Problem, limit: int) -> Optional[Node]:
    """Depth-limited search implementation.

    The algorithm treats nodes at depth == limit as if they have no children.
    It is important to notice that if the deepest level of the tree is, for example, 3,
    calling this function with limit = 3 will return the cutoff node.

    Parameters
    ----------
    problem : Problem
        The problem which this implementation searches.
    limit : int
        Depth limit, if a node is in a larger depth than this limit,
        the algorithm treats it like it doesn't have any children.

    Returns
    -------
    Node
        Solution node, if the function finds one, if the depth of the problem's
        tree is larger than the provided limit, the function returns a cutoff node
        which means there might be a solution in a deeper level.
        If there is no solution, the function returns None.
    """
    result = None

    frontier = deque([Node(state=problem.initial_state)])

    while frontier:
        node = frontier.pop()

        if problem.is_goal(node.state):
            return node
        elif node.depth >= limit:
            result = cutoff
        elif not node.is_cycle():
            frontier.extend([n for n in node.expand(problem)])

    return result


def iterative_deepening_search(problem: Problem) -> Optional[Node]:
    """Iterative-deepening search implementation.

    Calls depth-limited search with an ever increasing limit,
    until either a solution is found or the algorithm returns None
    because no solution exists.


    Parameters
    ----------
    problem : Problem
        The problem which this implementation searches.

    Returns
    -------
    Node
        Solution node, if the function finds one, else None.
    """
    depth = 0

    while True:
        node = depth_limited_search(problem, depth)

        if node is None or node != cutoff:
            return node
        depth += 1


def bidirectional_best_first_search(
        problem_f: Problem,
        evaluation_function_f: Callable[[Node], float],
        problem_b: Problem,
        evaluation_function_b: Callable[[Node], float],
        has_terminated: Callable[[Node, list[(float, Node)], list[(float, Node)]], bool]) -> Node:
    """Bidirectional best-first search implementation.

    This implementation is abstract in terms of it needing two evaluation functions and a function
    to check for termination passed in.
    The algorithm works by taking two problems, one in the forwards direction and one in the backwards.
    It maintains two frontiers and two reached dictionaries for each direction.
    The algorithm terminates when the two reached mappings have the same state in both of them.
    This check, however, is done in the proceed helper function.
    The algorithm needs the additional termination check for the cases where the evaluation functions are not the
    path costs of nodes.

    Parameters
    ----------
    problem_f : Problem
        Problem in the forwards direction (Initial -> Goal)
    evaluation_function_f : Callable[[Node], float]
        Cost evaluation function for the forwards problem.
    problem_b : Problem
        Problem in the backwards direction (Goal -> Initial)
    evaluation_function_b : Callable[[Node], float]
        Cost evaluation function for the backwards problem.
    has_terminated : Callable[[Node, list[(float, Node)], list[(float, Node)]], bool]
        Function that check if the found solution is an optimal one.

    Returns
    -------
    Node
        Solution node or failure.
    """
    node_f = Node(problem_f.initial_state)
    node_b = Node(problem_b.initial_state)

    frontier_f = []
    frontier_b = []
    heapq.heappush(frontier_f, (node_f.path_cost, node_f))
    heapq.heappush(frontier_b, (node_b.path_cost, node_b))

    reached_f = {}
    reached_b = {}

    solution = failure

    while not has_terminated(solution, frontier_f, frontier_b):
        solution = (proceed("F", problem_f, frontier_f, reached_f, reached_b, solution)
                    if evaluation_function_f(frontier_f[0][1]) < evaluation_function_b(frontier_b[0][1])
                    else proceed("B", problem_b, frontier_b, reached_b, reached_f, solution))

    return solution
