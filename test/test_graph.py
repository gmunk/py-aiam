import unittest

from graph import Graph


class TestGraph(unittest.TestCase):
    def test_get_nodes(self):
        connections = [("A", "B"), ("A", "C"), ("B", "D"), ("D", "E")]
        test_data = [(True, ["A", "B", "D"]), (False, ["A", "B", "C", "D", "E"])]

        for d, e in test_data:
            with self.subTest("Should have contained the correct nodes.", d=d, e=e):
                graph = Graph(connections, d)

                self.assertEqual(graph.get_nodes(), e)
