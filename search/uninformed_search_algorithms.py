from typing import Callable

from datastructures import PriorityQueue
from problem.node import Node, failure
from problem.problem import Problem
from search.helpers import path_cost_evaluation_function, proceed

EvaluationFunction = Callable[[Node], float]
HasTerminated = Callable[[Node, PriorityQueue, PriorityQueue], bool]


def best_first_search(problem: Problem, evaluation_function: EvaluationFunction) -> Node:
    """Best-first search implementation.

    A general implementation of the best-first search algorithm, specifying different evaluation functions
    provide different algorithms.

    Parameters
    ----------
    problem : Problem
        Problem, which the algorithm searches.
    evaluation_function: Callable[[Node], float]
        Function calculating the cost of each node.
        It is used in terms of the priority queue backing the algorithm.

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


def bidirectional_best_first_search(
        problem_f: Problem,
        evaluation_function_f: EvaluationFunction,
        problem_b: Problem,
        evaluation_function_b: EvaluationFunction,
        has_terminated: HasTerminated) -> Node:
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
