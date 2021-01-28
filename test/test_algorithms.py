import string
import unittest
from pathlib import Path

from search.algorithms import (best_first_search, breadth_first_search, depth_first_search, depth_limited_search)
from search.problem import (create_road_map_problem, create_tree_problem)


class TestSearchAlgorithm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if cls is TestSearchAlgorithm:
            raise unittest.SkipTest("%s is an abstract base class" % cls.__name__)
        else:
            super(TestSearchAlgorithm, cls).setUpClass()

    def setUp(self):
        self.test_data = []
        self.problem = None
        self.algorithm = None

    def test_algorithm(self):
        for g, p in self.test_data:
            with self.subTest("The computed path to the goal is incorrect.", g=g, p=p):
                self.problem.goal_states = g

                node = self.algorithm(self.problem)
                self.assertEqual(node.get_path(), p)


class TestBestFirstSearch(TestSearchAlgorithm):
    @classmethod
    def setUpClass(cls):
        with Path(__file__).parent.joinpath("resources", "romania_problem.json").open("r") as f:
            cls.problem = create_road_map_problem(f)

    def setUp(self):
        self.test_data = [({"Bucharest"}, ["Pitesti", "RimnicuVilcea", "Sibiu", "Arad"]),
                          ({"Craiova"}, ["RimnicuVilcea", "Sibiu", "Arad"]),
                          ({"Arad"}, [])]
        self.algorithm = best_first_search


class TestBreadthFirstSearch(TestSearchAlgorithm):
    @classmethod
    def setUpClass(cls):
        with Path(__file__).parent.joinpath("resources", "romania_problem.json").open("r") as f:
            cls.problem = create_road_map_problem(f)

    def setUp(self):
        self.test_data = [({"Bucharest"}, ["Fagaras", "Sibiu", "Arad"]),
                          ({"Craiova"}, ["RimnicuVilcea", "Sibiu", "Arad"]),
                          ({"Arad"}, [])]
        self.algorithm = breadth_first_search


class TestDepthFirstSearch(TestSearchAlgorithm):
    def setUp(self):
        self.test_data = [({"M"}, ["F", "C", "A"])]
        self.problem = create_tree_problem(list(string.ascii_uppercase[:15]), initial_state="A")
        self.algorithm = depth_first_search


# class TestDepthLimitedSearch(TestSearchAlgorithm):
#     __test__ = True
#
#     def test_algorithm(self):
#         test_data = [(3, {"E"}, ["B", "A"])]
#         problem = create_tree_problem(list(string.ascii_uppercase[:15]), initial_state="A")
#
#         for l, g, p in test_data:
#             with self.subTest("The computed path to the goal is incorrect.", l=l, g=g, p=p):
#                 self.assertEqual(depth_limited_search(problem, l), p)

