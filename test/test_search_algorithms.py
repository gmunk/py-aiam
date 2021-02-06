import unittest

from graph import romania_road_map
from problem.problem import GraphProblem
from search.algorithms import best_first_search, breadth_first_search


class TestSearchAlgorithms(unittest.TestCase):
    def test_best_first_search(self):
        test_data = [("Arad", {"Bucharest"}, ["Pitesti", "Rimnicu Vilcea", "Sibiu", "Arad"]),
                     ("Arad", {"Craiova"}, ["Rimnicu Vilcea", "Sibiu", "Arad"]),
                     ("Arad", {"Arad"}, [])]

        self.__with_graph_problem(test_data, best_first_search)

    def test_breadth_first_search(self):
        test_data = [("Arad", {"Bucharest"}, ["Fagaras", "Sibiu", "Arad"]),
                     ("Arad", {"Craiova"}, ["Rimnicu Vilcea", "Sibiu", "Arad"]),
                     ("Arad", {"Arad"}, [])]

        self.__with_graph_problem(test_data, breadth_first_search)

    def __with_graph_problem(self, test_data, algorithm):
        for i, g, e in test_data:
            with self.subTest("Should have returned the correct path to the goal.", i=i, g=g, e=e):
                romanian_road_map_problem = GraphProblem(i, g, romania_road_map)

                node = algorithm(romanian_road_map_problem)

                self.assertEqual(node.get_path(), e)
