from abc import ABC, abstractmethod
from collections import namedtuple

Action = namedtuple("Action", ["name", "cost"])

Node = namedtuple("Node", ["state", "parent", "action", "path_cost"])


class Problem(ABC):
    """
    An abstract class acting as the template for specifying search problems.

    Attributes
    ----------
    states : set
        A set of all the states comprising the environment this problem is concerned with.
    initial_state : any
        Initial state that the agent starts in.
    goal_states : set
        A set of one or more goal states.
    actions : dict
        A mapping of the actions available to the agent solving this problem,
        it's defined as a state (s) -> set of states, with the target being
        a finite set of actions that can be executed in s.
    """

    def __init__(self, states=None, initial_state=None, goal_states=None, actions=None):
        self.states = states if states is not None else set()
        self.initial_state = initial_state
        self.goal_states = goal_states if goal_states is not None else set()
        self.actions = actions if actions is not None else {}

    def is_goal(self, state):
        return state in self.goal_states

    @abstractmethod
    def apply_action(self, action):
        pass


class RomanianRoadMapProblem(Problem):
    def apply_action(self, action):
        return action.name[2:]


class TreeProblem(Problem):
    def apply_action(self, action):
        return action
