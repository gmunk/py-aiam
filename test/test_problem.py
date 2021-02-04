import unittest
from unittest.mock import patch, Mock

from graph import Graph
from search.problem import Problem, GraphProblem


class TestProblem(unittest.TestCase):
    @patch("search.problem.Problem.__abstractmethods__", set())
    def setUp(self):
        self.problem = Problem("S1", {"S3"})

    def test_is_goal(self):
        test_data = [("S3", True), ("S1", False)]

        for s, e in test_data:
            with self.subTest("Should have determined that the provided state is a goal state",
                              s=s, e=e):
                self.assertEqual(self.problem.is_goal(s), e)


class TestGraphProblem(unittest.TestCase):
    def setUp(self):
        self.mock_graph = Mock(spec_set=Graph)
        self.mock_graph.get_nodes.return_value = {"S1", "S2", "S3", "S4"}

        self.problem = GraphProblem("S1", {"S3"}, self.mock_graph)

    def test_get_actions(self):
        test_data = [("S1", {("S2", 1), ("S3", 1)}), ("S4", set())]

        for s, e in test_data:
            with self.subTest("Should have returned the correct actions", s=s, e=e):
                self.mock_graph.get_connections.return_value = e
                self.assertEqual(self.problem.get_actions(s), e)

    def test_apply_action(self):
        valid_action, valid_expected = (("S1", 1), "S1")
        invalid_action = ("S5", 1)

        with self.subTest("Should have applied the action as expected.",
                          valid_action=valid_action,
                          valid_expected=valid_expected):
            self.assertEqual(self.problem.apply_action(valid_action), valid_expected)

        with self.subTest("Should have raised an exception.", invalid_action=invalid_action):
            self.assertRaises(ValueError, self.problem.apply_action, invalid_action)

    def test_get_action_cost(self):
        valid_action, valid_expected = (("S1", 1), 1)
        invalid_action = ("S5", 1)

        with self.subTest("Should have applied the action as expected.",
                          valid_action=valid_action,
                          valid_expected=valid_expected):
            self.assertEqual(self.problem.get_action_cost(valid_action), valid_expected)

        with self.subTest("Should have raised an exception.", invalid_action=invalid_action):
            self.assertRaises(ValueError, self.problem.get_action_cost, invalid_action)
