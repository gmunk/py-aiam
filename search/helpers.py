from datastructures import PriorityQueue
from problem.node import Node, join_nodes
from problem.problem import Problem


def path_cost_evaluation_function(node: Node):
    return node.path_cost


def proceed(direction: str,
            problem: Problem,
            frontier: PriorityQueue,
            reached1: dict[str, Node],
            reached2: dict[str, Node],
            solution: Node) -> Node:
    node = frontier.pop()[1]

    for c in node.expand(problem):
        state = c.state

        if state not in reached1 or c.path_cost < reached1[state].path_cost:
            reached1[state] = c
            frontier.add(c)

            if state in reached2:
                joined_solution = join_nodes(direction, (c, reached2[state]))
                if joined_solution.path_cost < solution.path_cost:
                    solution = joined_solution

    return solution
