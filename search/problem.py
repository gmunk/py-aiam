from abc import ABC, abstractmethod
from dataclasses import dataclass

DEFAULT_PATH_COST = 0


@dataclass(frozen=True, eq=True)
class Action:
    name: str = None
    cost: int = DEFAULT_PATH_COST


@dataclass(frozen=True, eq=True)
class Node:
    state: str = None
    parent: "Node" = None
    action: "Action" = None
    path_cost: int = DEFAULT_PATH_COST


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

    def is_goal(self, node):
        return node.state in self.goal_states

    @abstractmethod
    def apply_action(self, action):
        pass


class RomanianRoadMapProblem(Problem):
    def apply_action(self, action):
        return action.name[2:]


class TreeProblem(Problem):
    def apply_action(self, action):
        return action.name


def get_path_to(node):
    path = []

    while node:
        path.append(node.state)
        node = node.parent

    return path
