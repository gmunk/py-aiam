import json
import unittest
from collections import defaultdict
from search.problem import Action, RomanianRoadMapProblem
from search.node import Node
from search.search import DEFAULT_PRIORITY, expand, best_first_search


class TestSearchAlgorithms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("resources/romania_problem.json") as f:
            problem_json = json.load(f)

            cls.states = set()
            cls.initial_state = problem_json["initial_state"]
            cls.goal_states = set(problem_json["goal_states"])
            cls.actions = defaultdict(set)

            for s in problem_json["states"]:
                cls.states.add(s["name"])
                for a in s["actions"]:
                    cls.actions[s["name"]].add(Action(a["name"], a["cost"]))

    def setUp(self):
        self.problem = RomanianRoadMapProblem(states=self.states,
                                              initial_state=self.initial_state,
                                              goal_states=self.goal_states,
                                              actions=self.actions)

    def test_best_first_search(self):
        node = best_first_search(self.problem)

        self.assertTrue(node.state in self.problem.goal_states)

    def test_expand(self):
        node = Node(state="Arad", path_cost=DEFAULT_PRIORITY)
        expected = {"Zerind", "Sibiu", "Timisoara"}

        for n in expand(self.problem, node):
            self.assertTrue(n.state in expected)
