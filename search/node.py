DEFAULT_PATH_COST = 0
DEFAULT_DEPTH = 0


class Node:
    """Represents a node in a graph (tree) of a problem.

    Parameters
    ----------
    state : str
        The state which this node represents.
    parent : Node
        Parent of this node.
    action : Action
        The action executed to reach this node.
    path_cost : int
        Path cost, from the root, to this node.
    """
    def __init__(self, state=None, parent=None, action=None, path_cost=DEFAULT_PATH_COST):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = DEFAULT_DEPTH if parent is None else parent.depth + 1

    def __eq__(self, other):
        return self.state == other.state \
               and self.parent == other.parent \
               and self.action == other.action \
               and self.path_cost == other.path_cost \
               and self.depth == other.depth

    def get_path(self):
        """Returns the path from this node to the root (omitting this node).

        For example if this is node C and the path is "A" -> "B" -> "C", this function will return
        a list–["B", "A"]

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


cutoff = Node(state="cutoff")
