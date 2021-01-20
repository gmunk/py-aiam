import unittest

from search.algorithms import (best_first_search, breadth_first_search)
from search.problem import (get_path_to, create_road_map_problem)


class TestSearchAlgorithm(unittest.TestCase):
    __test__ = False

    def setUp(self):
        self.test_data = []
        self.problem = None
        self.algorithm = None

    def test_algorithm(self):
        for g, p in self.test_data:
            with self.subTest("The computed path to the goal is incorrect.", g=g, p=p):
                self.problem.goal_states = g

                node = self.algorithm(self.problem)
                self.assertEqual(get_path_to(node), p)


class TestBestFirstSearch(TestSearchAlgorithm):
    __test__ = True

    @classmethod
    def setUpClass(cls):
        with open("resources/romania_problem.json") as f:
            cls.problem = create_road_map_problem(f)

    def setUp(self):
        self.test_data = [({"Bucharest"}, ["Bucharest", "Pitesti", "RimnicuVilcea", "Sibiu", "Arad"]),
                          ({"Craiova"}, ["Craiova", "RimnicuVilcea", "Sibiu", "Arad"]),
                          ({"Arad"}, ["Arad"])]
        self.algorithm = best_first_search


class TestBreadthFirstSearch(TestSearchAlgorithm):
    __test__ = True

    @classmethod
    def setUpClass(cls):
        with open("resources/romania_problem.json") as f:
            cls.problem = create_road_map_problem(f)

    def setUp(self):
        self.test_data = [({"Bucharest"}, ["Bucharest", "Fagaras", "Sibiu", "Arad"]),
                          ({"Craiova"}, ["Craiova", "RimnicuVilcea", "Sibiu", "Arad"]),
                          ({"Arad"}, ["Arad"])]
        self.algorithm = breadth_first_search
