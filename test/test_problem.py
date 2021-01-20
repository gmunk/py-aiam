import unittest
from unittest.mock import patch

from search.problem import Problem, Node


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
        test_data = [(Node(state="s3"), True), (Node(state="s1"), False)]

        for n, e in test_data:
            with self.subTest(n=n, e=e):
                self.assertEqual(self.problem.is_goal(n), e)





