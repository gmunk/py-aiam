import unittest
import json
from unittest.mock import patch
from collections import defaultdict
from search.problem import Action, Problem, RomanianRoadMapProblem


class TestProblem(unittest.TestCase):
    @patch("search.problem.Problem.__abstractmethods__", set())
    def setUp(self):
        self.problem = Problem(states={"s1", "s2", "s3", "s4"},
                               initial_state="s1",
                               goal_states={"s3"},
                               actions={"s1": {"a2"},
                                        "s2": {"a1", "a4"},
                                        "s4": {"a2", "a3"},
                                        "s3": {"a4"}})

    def test_is_goal(self):
        test_data = [("s3", True), ("s1", False)]

        for s, g in test_data:
            with self.subTest(s=s, g=g):
                self.assertEqual(self.problem.is_goal(s), g)


class TestRomanianRoadProblem(unittest.TestCase):
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

    def test_apply_action(self):
        test_data = [("Arad", Action("ToSibiu", 140), "Sibiu"), ("Sibiu", Action("ToArad", 140), "Arad")]

        for s, a, e in test_data:
            with self.subTest(s=s, a=a, e=e):
                state = self.problem.apply_action(s, a)
                self.assertEqual(state, e)