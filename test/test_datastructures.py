import math
import unittest

from datastructures import Graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.connections = [("A", "B"), ("A", "C"), ("B", "D"), ("D", "E")]

    def test_get_nodes(self):
        test_data = [True, False]
        expected = {s for c in self.connections for s in c}

        for d in test_data:
            with self.subTest("Should have returned a correct set of nodes", d=d, e=expected):
                graph = Graph(self.connections, d)

                self.assertEqual(graph.get_vertices(), expected)

    def test_get_connections(self):
        test_data = [(self.connections[0][0], set([(c[1], math.inf) for c in self.connections[:2]])), ("Z", set())]

        graph = Graph(self.connections)

        for n, e in test_data:
            with self.subTest("Should have returned the correct connections.", n=n, e=e):
                self.assertEqual(graph.get_edges(n), e)
