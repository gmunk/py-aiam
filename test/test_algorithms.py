import string
import unittest
from pathlib import Path

from search.algorithms import (best_first_search, breadth_first_search, depth_first_search, depth_limited_search,
                               iterative_deepening_search)
from search.node import cutoff
from search.problem import (create_road_map_problem, create_tree_problem)


class TestSearchAlgorithm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if cls is TestSearchAlgorithm:
            raise unittest.SkipTest("{} is an abstract base class".format(cls.__name__))
        else:
            super(TestSearchAlgorithm, cls).setUpClass()

    def setUp(self):
        self.test_data = []
        self.problem = None
        self.algorithm = None

    def test_algorithm(self):
        for g, p in self.test_data:
            with self.subTest("Should have returned a correct path to the goal.", g=g, p=p):
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


class TestDepthLimitedSearch(unittest.TestCase):
    def test_algorithm(self):
        test_data = [(2, {"E"}, ["B", "A"]), (2, {"B"}, ["A"]), (2, {"A"}, [])]

        cl, cg = (2, {"K"})

        problem = create_tree_problem(list(string.ascii_uppercase[:15]), initial_state="A")

        for lim, g, p in test_data:
            with self.subTest("Should have returned a correct path to the goal.", lim=lim, g=g, p=p):
                problem.goal_states = g

                node = depth_limited_search(problem, lim)
                self.assertEqual(node.get_path(), p)

        with self.subTest("Should have returned a cutoff, meaning a solution might be found deeper than the limit.", lim=cl, g=cg):
            problem.goal_states = cg

            node = depth_limited_search(problem, cl)
            self.assertEqual(node, cutoff)


class TestIterativeDeepeningSearch(TestSearchAlgorithm):
    def setUp(self):
        self.test_data = [({"M"}, ["F", "C", "A"])]
        self.problem = create_tree_problem(list(string.ascii_uppercase[:15]), initial_state="A")
        self.algorithm = iterative_deepening_search
