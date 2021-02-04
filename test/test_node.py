import unittest

from search.node import Node


class TestNode(unittest.TestCase):
    def setUp(self):
        self.root = Node(state="root")
        self.first = Node(state="first",
                          parent=self.root)
        self.second = Node(state="second",
                           parent=self.first)

    def test_get_path(self):
        test_data = [(self.second, [self.first.state, self.root.state]),
                     (self.first, [self.root.state]),
                     (self.root, [])]

        for n, p in test_data:
            with self.subTest("The path to the node is incorrect.", n=n, p=p):
                self.assertEqual(n.get_path(), p)

    def test_is_cycle(self):
        cycle_node = Node(state=self.second.state, parent=self.root, action=self.second.action)
        self.first.parent = cycle_node

        test_data = [(self.second, True), (self.first, False), (self.root, False)]

        for n, e in test_data:
            with self.subTest("Incorrectly determined if node is on a cycle path", n=n, e=e):
                self.assertEqual(n.is_cycle(), e)
