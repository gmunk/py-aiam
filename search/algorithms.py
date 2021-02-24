import heapq
from collections import deque
from typing import Optional

from problem.node import Node, cutoff
from problem.problem import Problem


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
    problem.node.Node
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
    problem.node.Node
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
    problem.node.Node
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
    problem.node.Node
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
    problem.node.Node
        Solution node, if the function finds one, else None.
    """
    depth = 0

    while True:
        node = depth_limited_search(problem, depth)

        if node is None or node != cutoff:
            return node
        depth += 1


def bidirectional_best_first_search(problem_f: Problem, problem_b: Problem) -> Optional[Node]:
    def has_terminated(s: Optional[Node], f_f: list[(float, Node)], f_b: list[(float, Node)]) -> bool:
        # Front and Back nodes, this has to be refactored. Maybe create a custom data structure.
        f, b = f_f[0][1], f_b[0][1]
        return s and f.path_cost + b.path_cost > s.path_cost

    def join_nodes(direction, nodes: tuple[Node, Node]) -> Node:
        f, b = nodes if direction == "F" else nodes[::-1]

        join_node = f

        while b.parent is not None:
            cost = join_node.path_cost + b.path_cost - b.parent.path_cost
            join_node = Node(b.parent.state, join_node, b.parent.action, cost)
            b = b.parent

        return join_node

    def proceed(direction,
                problem: Problem,
                frontier: list[(float, Node)],
                reached1: dict[str, Node],
                reached2: dict[str, Node],
                solution: Optional[Node]):
        n = heapq.heappop(frontier)

        for c in n.expand(problem):
            state = c.state
            if state not in reached1 or c.path_cost < reached1[state].path_cost:
                reached1[state] = c
                heapq.heappush(frontier, (c.path_cost, c))
                if state in reached2:
                    joined_solution = join_nodes(direction, (c, reached2[state]))
                    if joined_solution.path_cost < solution.path_cost:
                        solution = joined_solution

        return solution

    node_f = Node(problem_f.initial_state)
    node_b = Node(problem_b.initial_state)

    frontier_f = []
    frontier_b = []
    heapq.heappush(frontier_f, (node_f.path_cost, node_f))
    heapq.heappush(frontier_b, (node_b.path_cost, node_b))

    reached_f = {}
    reached_b = {}

    result = None

    while not has_terminated(result, frontier_f, frontier_b):
        if frontier_f[0][1].path_cost < frontier_b[0][1]:
            result = (proceed("F", problem_f, frontier_f, reached_f, reached_b, result)
                      if frontier_f[0][1].path_cost < frontier_b[0][1].path_cost
                      else proceed("B", problem_b, frontier_b, reached_b, reached_f, result))

    return result
