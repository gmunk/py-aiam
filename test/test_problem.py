import unittest
from unittest.mock import patch

from search.node import Node, Action
from search.problem import Problem, RoadMapProblem


class TestProblem(unittest.TestCase):
    @patch("search.problem.Problem.__abstractmethods__", set())
    def setUp(self):
        self.problem = Problem(states={"S1", "S2", "S3", "S4"},
                               goal_states={"S3"})

    def test_is_goal(self):
        test_data = [(Node(state="S3"), True), (Node(state="S1"), False)]

        for n, e in test_data:
            with self.subTest(n=n, e=e):
                self.assertEqual(self.problem.is_goal(n), e)


class TestRoadMapProblem(unittest.TestCase):
    def setUp(self):
        self.problem = RoadMapProblem(states={"S1", "S2"},
                                      actions={"S1": {Action(name="ToS2")}})

    def test_apply_action(self):
        valid_action, valid_expected = (Action(name="ToS2"), "S2")
        invalid_action, invalid_expected = (Action(name="ToS3"), "S3")

        with self.subTest("Incorrect state after applying an action.",
                          valid_action=valid_action,
                          valid_expected=valid_expected):
            self.assertEqual(self.problem.apply_action(valid_action), valid_expected)

        with self.subTest("Should have raised an exception when applying an incorrect action",
                          invalid_action=invalid_action,
                          invalid_expected=invalid_expected):
            self.assertRaises(ValueError, self.problem.apply_action, invalid_action)

