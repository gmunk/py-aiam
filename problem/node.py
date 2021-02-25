from __future__ import annotations

import math
from typing import Any, Generator

DEFAULT_PATH_COST = 0
DEFAULT_DEPTH = 0


class Node:
    """Represents a node in a graph (tree) of a problem.

    Parameters
    ----------
    state : Any
        The state which this node represents.
    parent : problem.node.Node
        Parent of this node.
    action : tuple[str, float]
        The action executed to reach this node.
    path_cost : float
        Path cost, from the root, to this node.
    """

    def __init__(self,
                 state: Any = None,
                 parent: Node = None,
                 action: tuple[str, float] = None,
                 path_cost: float = DEFAULT_PATH_COST) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = DEFAULT_DEPTH if parent is None else parent.depth + 1

    def __eq__(self, other):
        return (self.state == other.state
                and self.parent == other.parent
                and self.action == other.action
                and self.path_cost == other.path_cost
                and self.depth == other.depth)

    def get_path(self):
        """Returns the path from this node to the root (omitting this node).

        For example if this is node C and the path is "A" -> "B" -> "C",
        this function will return a list–["B", "A"]

        Returns
        -------
        List
            The path from this node to the root.

        """
        path = []

        p = self.parent
        while p:
            path.append(p.state)
            p = p.parent

        return path

    def is_cycle(self):
        """Determines if the current node is on a cycle path.

        Returns
        -------
        Bool
            Whether this node is on a cycle path.
        """
        path = self.get_path()
        return any(s == self.state for s in path)

    def expand(self, problem) -> Generator[Node]:
        """Expands the nodes that are one step away from this one.

        This function also calculates the path cost from the root to each node it expands,
        if the action to reach an expanded node doesn't have a cost (represented as math.inf),
        it sets the expanded path cost to the parent's path cost (this node it the parent).

        Parameters
        ----------
        problem : Problem
            The problem which this node is a part of.

        Yields
        -------
        Node
            A descendant, one step away, of this node.
        """
        for a in problem.get_actions(self.state):
            frontier_state = problem.apply_action(a)
            cost = self.path_cost if a[1] == math.inf else self.path_cost + a[1]

            yield Node(state=frontier_state, parent=self, action=a, path_cost=cost)


def join_nodes(direction: str, nodes: tuple[Node, Node]) -> Node:
    n_f, n_b = nodes if direction == "F" else nodes[::-1]

    join_node = n_f

    while n_b.parent is not None:
        cost = join_node.path_cost + n_b.path_cost - n_b.parent.path_cost
        join_node = Node(n_b.parent.state, join_node, n_b.parent.action, cost)
        n_b = n_b.parent

    return join_node


cutoff = Node(state="cutoff", path_cost=math.inf)
failure = Node(state="failure", path_cost=math.inf)
