from collections import deque
from typing import Callable

from datastructures import PriorityQueue
from problem.node import Node, failure, cutoff
from problem.problem import Problem
from search.helpers import path_cost_evaluation_function, proceed

EvaluationFunction = Callable[[Node], float]
HasTerminated = Callable[[Node, PriorityQueue, PriorityQueue], bool]


def best_first_search(problem: Problem, evaluation_function: EvaluationFunction) -> Node:
    """Best-first search implementation.

    A general implementation of the best-first search algorithm,
    specifying different evaluation functions provides different algorithms.

    Parameters
    ----------
    problem : Problem
        Problem, which the algorithm searches.
    evaluation_function: Callable[[Node], float]
        Function calculating the cost of each node. It is used to order the priority queue backing the algorithm.

    Returns
    -------
    Node
        Solution node or failure.
    """
    node = Node(state=problem.initial_state)

    reached = {node.state: node}
    frontier = PriorityQueue([(evaluation_function(node), node)], evaluation_function)

    while frontier:
        n = frontier.pop()[1]

        if problem.is_goal(n.state):
            return n
        for c in n.expand(problem):
            if c.state not in reached or c.path_cost < reached[c.state].path_cost:
                reached[c.state] = c
                frontier.add(node)

    return failure


def uniform_cost_search(problem: Problem) -> Node:
    """Uniform-cost search implementation. (Dijkstra's algorithm)

    This implementation calls best-first search with an evaluation function which
    is the path cost of a node. By doing this, the algorithm ensures that it takes the optimal path
    to reach a solution.

    Parameters
    ----------
    problem : Problem
        Problem, which the algorithm searches.

    Returns
    -------
    Node
        Solution node or failure.
    """
    return best_first_search(problem, path_cost_evaluation_function)


def breadth_first_search(problem: Problem) -> Node:
    """Breadth-first search implementation.

    Relies on the dequeue data structure for its FIFO queue needs.
    Goal checking happens immediately after the while loop reaches a node.
    Contrast this with best-first search which performs a late goal test,
    after a node is popped from its priority queue.

    Parameters
    ----------
    problem : Problem
        The problem which this implementation searches.

    Returns
    -------
    Node
        Solution node or failure.
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

    return failure


def depth_first_search(problem: Problem) -> Node:
    """Depth-first search implementation.

    Relies on the dequeue data structure for its need of a LIFO queue.

    Parameters
    ----------
    problem: Problem
        The problem which this implementation searches.

    Returns
    -------
    Node
        Solution node or failure.
    """
    frontier = deque([Node(state=problem.initial_state)])

    while frontier:
        node = frontier.pop()

        if problem.is_goal(node.state):
            return node

        frontier.extend([n for n in node.expand(problem)])

    return failure


def depth_limited_search(problem: Problem, limit: int) -> Node:
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
        If there is no solution, the function returns failure.
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


def iterative_deepening_search(problem: Problem) -> Node:
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

        if node != cutoff:
            return node
        depth += 1


def bidirectional_best_first_search(
        problem_f: Problem,
        evaluation_function_f: EvaluationFunction,
        problem_b: Problem,
        evaluation_function_b: EvaluationFunction,
        has_terminated: HasTerminated) -> Node:
    """Bidirectional best-first search implementation.

    Abstract implementation which has configurable behaviour.
    Passing different evaluation and termination functions provides a different algorithm.

    Works by taking two problems, one in the forwards direction and one in the backwards.
    It maintains two frontiers and two reached dictionaries for each direction.
    The algorithm terminates when the two reached mappings have the same state in both of them.
    This check is done in the proceed helper function.

    Performs an extra termination check for the cases where the evaluation functions are not the path costs of nodes.

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

    frontier_f = PriorityQueue([(evaluation_function_f(node_f), node_f)], evaluation_function_f)
    frontier_b = PriorityQueue([(evaluation_function_f(node_b), node_b)], evaluation_function_b)

    reached_f = {}
    reached_b = {}

    solution = failure

    while not has_terminated(solution, frontier_f, frontier_b):
        solution = (proceed("F", problem_f, frontier_f, reached_f, reached_b, solution)
                    if evaluation_function_f(frontier_f.top()) < evaluation_function_b(frontier_b.top())
                    else proceed("B", problem_b, frontier_b, reached_b, reached_f, solution))

    return solution
