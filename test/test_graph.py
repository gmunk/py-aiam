import math
import unittest

from graph import Graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.connections = [("A", "B"), ("A", "C"), ("B", "D"), ("D", "E")]

    def test_get_nodes(self):
        expected = {s for c in self.connections for s in c}

        graph = Graph(self.connections)

        self.assertEqual(graph.get_nodes(), expected)

    def test_get_connections(self):
        test_data = [(self.connections[0][0], set([(c[1], math.inf) for c in self.connections[:2]])), ("Z", set())]

        graph = Graph(self.connections)

        for n, e in test_data:
            with self.subTest("Should have returned the correct connections.", n=n, e=e):
                self.assertEqual(graph.get_connections(n), e)
