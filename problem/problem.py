from abc import ABC, abstractmethod


class Problem(ABC):
    """An abstract class acting as the base for problem representations.

    Parameters
    ----------
    initial_state : obj
        The state from which an agent will begin solving this problem.
    goal_states : set
        A set of states which represents the target for an agent solving this problem.
    """

    def __init__(self, initial_state, goal_states: set):
        self.initial_state = initial_state
        self.goal_states = goal_states

    def is_goal(self, state):
        return state in self.goal_states

    @abstractmethod
    def get_actions(self, state):
        pass

    @abstractmethod
    def apply_action(self, action):
        pass

    @abstractmethod
    def get_action_cost(self, action):
        pass


class GraphProblem(Problem):
    """Representation of a graph problem.

    Parameters
    ----------
    graph : graph.Graph
        The internal graph data structure holding the data for this problem.
    """

    def __init__(self, initial_state, goal_states, graph):
        super().__init__(initial_state=initial_state, goal_states=goal_states)
        self.graph = graph

    def get_actions(self, state):
        return self.graph.get_connections(state)

    def apply_action(self, action):
        if action[0] not in self.graph.get_nodes():
            raise ValueError
        return action[0]

    def get_action_cost(self, action):
        if action[0] not in self.graph.get_nodes():
            raise ValueError
        return action[1]
