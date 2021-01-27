import json
from abc import ABC, abstractmethod
from collections import defaultdict

from search.node import Action


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


class RoadMapProblem(Problem):
    def apply_action(self, action):
        state = action.name[2:]

        if state not in self.states:
            raise ValueError
        return state


class TreeProblem(Problem):
    def apply_action(self, action):
        return action.name


def create_road_map_problem(file):
    problem_json = json.load(file)

    states = set()
    actions = defaultdict(set)

    for s in problem_json["states"]:
        states.add(s["name"])
        for a in s["actions"]:
            actions[s["name"]].add(Action(a["name"], a["cost"]))

    return RoadMapProblem(states=states,
                          initial_state=problem_json["initial_state"],
                          goal_states=set(problem_json["goal_states"]),
                          actions=actions)


def create_tree_problem(states, initial_state=None, goal_states=None):
    number_parents = int(len(states) / 2)

    actions = {states[i]: set() for i in range(number_parents)}

    sts = states[1:]
    for i, k in enumerate(actions):
        actions[k].update([Action(name=s) for s in sts[i * 2:(i * 2) + 2]])

    return TreeProblem(
        states=set(states),
        initial_state=initial_state,
        goal_states=goal_states,
        actions=actions
    )
