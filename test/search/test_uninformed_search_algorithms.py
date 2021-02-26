import unittest

from datastructures import binary_tree, romania_road_map
from problem.node import cutoff, failure
from problem.problem import GraphProblem
from search.uninformed_search_algorithms import (uniform_cost_search, depth_limited_search, depth_first_search,
                                                 breadth_first_search, iterative_deepening_search)


class TestSearchAlgorithms(unittest.TestCase):
    def test_uniform_cost_search(self):
        test_data = [("Arad", {"Bucharest"}, ["Pitesti", "Rimnicu Vilcea", "Sibiu", "Arad"]),
                     ("Arad", {"Craiova"}, ["Rimnicu Vilcea", "Sibiu", "Arad"]),
                     ("Arad", {"Arad"}, []),
                     ("Arad", {"Unknown"}, failure)]

        self.__with_graph_problem(test_data, romania_road_map, uniform_cost_search)

    def test_breadth_first_search(self):
        test_data = [("Arad", {"Bucharest"}, ["Fagaras", "Sibiu", "Arad"]),
                     ("Arad", {"Craiova"}, ["Rimnicu Vilcea", "Sibiu", "Arad"]),
                     ("Arad", {"Arad"}, []),
                     ("Arad", {"Unknown"}, failure)]

        self.__with_graph_problem(test_data, romania_road_map, breadth_first_search)

    def test_depth_first_search(self):
        test_data = [("A", {"M"}, ["F", "C", "A"]), ("A", {"A"}, []), ("A", {"Z"}, failure)]

        self.__with_graph_problem(test_data, binary_tree, depth_first_search)

    def test_depth_limited_search(self):
        test_data = [("A", {"K"}, ["E", "B", "A"], 3),
                     ("A", {"A"}, [], 3),
                     ("A", {"K"}, cutoff, 2),
                     ("A", {"Z"}, failure, 4)]

        self.__with_graph_problem(test_data, binary_tree, depth_limited_search)

    def test_iterative_deepening_search(self):
        test_data = [("A", {"M"}, ["F", "C", "A"]), ("A", {"A"}, []), ("A", {"Z"}, failure)]

        self.__with_graph_problem(test_data, binary_tree, iterative_deepening_search)

    def __with_graph_problem(self, test_data, graph, algorithm):
        for i, g, e, *a in test_data:
            with self.subTest("Should have returned one of a solution, a cutoff or failure.", i=i, g=g, e=e, a=a):
                problem = GraphProblem(i, g, graph)

                node = algorithm(problem, *a)

                if type(e) != list:
                    self.assertEqual(node, e)
                else:
                    self.assertEqual(node.get_path(), e)
