import unittest
from unittest.mock import patch

from search.node import Node, Action
from search.problem import Problem, RoadMapProblem, EightQueensProblem


class TestProblem(unittest.TestCase):
    @patch("search.problem.Problem.__abstractmethods__", set())
    def setUp(self):
        self.problem = Problem(states={"S1", "S2", "S3", "S4"},
                               goal_states={"S3"})

    def test_is_goal(self):
        test_data = [("S3", True), ("S1", False)]

        for s, e in test_data:
            with self.subTest(s=s, e=e):
                self.assertEqual(self.problem.is_goal(s), e)


class TestRoadMapProblem(unittest.TestCase):
    def setUp(self):
        self.problem = RoadMapProblem(states={"S1", "S2"},
                                      actions={"S1": {Action(name="ToS2")}})

    def test_apply_action(self):
        valid_action, valid_expected = (Action(name="ToS2"), "S2")
        invalid_action, invalid_expected = (Action(name="ToS3"), "S3")

        with self.subTest("Should have applied the action correctly.",
                          valid_action=valid_action,
                          valid_expected=valid_expected):
            self.assertEqual(self.problem.apply_action(valid_action), valid_expected)

        with self.subTest("Should have raised an exception when applying an incorrect action",
                          invalid_action=invalid_action,
                          invalid_expected=invalid_expected):
            self.assertRaises(ValueError, self.problem.apply_action, invalid_action)


class TestEightQueensProblem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        queen_positions = [(3, 3), (4, 0), (4, 4), (5, 1), (5, 5), (5, 7), (6, 2), (6, 6)]
        initial_state = [[0] * 8 for i in range(8)]

        for p in queen_positions:
            initial_state[p[0]][p[1]] = -1

        cls.problem = EightQueensProblem(initial_state=initial_state)