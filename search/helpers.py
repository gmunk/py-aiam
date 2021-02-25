import heapq

from problem.node import Node, join_nodes
from problem.problem import Problem


def proceed(direction: str,
            problem: Problem,
            frontier: list[(float, Node)],
            reached1: dict[str, Node],
            reached2: dict[str, Node],
            solution: Node) -> Node:
    node = heapq.heappop(frontier)

    for c in node.expand(problem):
        state = c.state

        if state not in reached1 or c.path_cost < reached1[state].path_cost:
            reached1[state] = c
            heapq.heappush(frontier, (c.path_cost, c))

            if state in reached2:
                joined_solution = join_nodes(direction, (c, reached2[state]))
                if joined_solution.path_cost < solution.path_cost:
                    solution = joined_solution

    return solution
