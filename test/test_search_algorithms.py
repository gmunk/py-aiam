import unittest

from graph import romania_road_map, binary_tree
from problem.problem import GraphProblem
from search.algorithms import best_first_search, breadth_first_search, depth_first_search


class TestSearchAlgorithms(unittest.TestCase):
    def test_best_first_search(self):
        test_data = [("Arad", {"Bucharest"}, ["Pitesti", "Rimnicu Vilcea", "Sibiu", "Arad"]),
                     ("Arad", {"Craiova"}, ["Rimnicu Vilcea", "Sibiu", "Arad"]),
                     ("Arad", {"Arad"}, []),
                     ("Arad", {"Unknown"}, None)]

        self.__with_graph_problem(test_data, romania_road_map, best_first_search)

    def test_breadth_first_search(self):
        test_data = [("Arad", {"Bucharest"}, ["Fagaras", "Sibiu", "Arad"]),
                     ("Arad", {"Craiova"}, ["Rimnicu Vilcea", "Sibiu", "Arad"]),
                     ("Arad", {"Arad"}, []),
                     ("Arad", {"Unknown"}, None)]

        self.__with_graph_problem(test_data, romania_road_map, breadth_first_search)

    def test_depth_first_search(self):
        test_data = [("A", {"M"}, ["F", "C", "A"]), ("A", {"A"}, []), ("A", {"Z"}, None)]

        self.__with_graph_problem(test_data, binary_tree, depth_first_search)

    def __with_graph_problem(self, test_data, graph, algorithm):
        test_data_none = []
        for i, t in enumerate(test_data):
            if t[2] is None:
                test_data_none.append(t)
                test_data.pop(i)

        for i, g, e in test_data:
            with self.subTest("Should have returned the correct path to the goal.", i=i, g=g, e=e):
                problem = GraphProblem(i, g, graph)
                node = algorithm(problem)

                self.assertEqual(node.get_path(), e)

        for i, g, e in test_data_none:
            with self.subTest("Should have returned None since there is no solution", i=i, g=g, e=e):
                problem = GraphProblem(i, g, graph)
                node = algorithm(problem)

                self.assertIsNone(node)
