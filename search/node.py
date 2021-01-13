class Node:
    def __init__(self, state=None, parent=None, action=None, path_cost=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __str__(self):
        return f'Node(state={self.state}, parent={self.parent}, action={self.action}, path_cost={self.path_cost})'

    def __repr__(self):
        return f'Node(state={self.state}, parent={self.parent}, action={self.action}, path_cost={self.path_cost})'
