import heapq
from collections import deque

from search.node import Node, cutoff


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


def depth_limited_search(problem, limit):
    """Depth-limited search implementation.

    Parameters
    ----------
    problem : Problem
        The problem which this implementation searches.
    limit : Int
        Depth limit, if a node is in a larger depth than this limit,
        the algorithm treats it like it doesn't have any children.

    Returns
    -------
    Node
        The goal node, if the function finds a solution, if the depth of the problem's
        tree is larger than the function returns a cutoff node
        which means there might be a solution in a deeper level.
        If the algorithm doesn't find a solution, it returns None.
    """
    result = None

    frontier = deque([Node(state=problem.initial_state)])

    while frontier:
        node = frontier.pop()

        if problem.is_goal(node):
            return node
        if node.get_depth() >= limit:
            result = cutoff
        elif not node.is_cycle():
            for n in expand(problem, node):
                frontier.append(n)

    return result


def iterative_deepening_search(problem):
    """Iterative-deepening search implementation.

    This algorithm uses depth-limited search with a different limit, starting from zero and incrementing up.


    Parameters
    ----------
    problem : Problem
        The problem which this implementation searches.

    Returns
    -------
    Node
        The goal node, if the function finds a solution, else None.
    """
    depth = 0

    while True:
        node = depth_limited_search(problem, depth)
        if node != cutoff:
            return node
        depth += 1


# --- NOT READY ---
def bidirectional_best_first_search(problem):
    forwards_dir = "F"
    backwards_dir = "B"

    def is_terminated(r, ff, fb):
        return r is not None and ff.pop().path_cost + fb.pop().path_cost > r.path_cost

    def proceed(d, p, f, r1, r2, r):
        node = f.pop()

        for n in expand(p, node):
            if n.state not in r1 or n.path_cost < r1[n.state].path_cost:
                r1[n.state] = n
                heapq.heappush(f, (n.path_cost, n))
                if n.state in r2:
                    pass

        return r

    result = None

    node_forwards = Node(state=problem.initial_state)

    frontier_forwards = []
    heapq.heappush(frontier_forwards, (node_forwards.path_cost, node_forwards))

    reached_forwards = {node_forwards.state: node_forwards}

    frontier_backwards, reached_backwards = [], {}

    for gs in problem.goal_states:
        node_backwards = Node(state=gs)
        heapq.heappush(frontier_backwards, (node_backwards.path_cost, node_backwards))

        reached_backwards[node_backwards.state] = node_backwards

    while not is_terminated(result, frontier_forwards, frontier_backwards):
        result = proceed(forwards_dir, problem, frontier_forwards, reached_forwards, reached_backwards, result) \
            if frontier_forwards.pop().path_cost < frontier_backwards.pop().path_cost \
            else proceed(backwards_dir, problem, frontier_backwards, reached_backwards, reached_forwards, result)

    return result
