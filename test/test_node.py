from unittest import TestCase
from unittest.mock import Mock

from search.node import Node
from search.problem import Problem


class TestNode(TestCase):
    def setUp(self):
        self.node = Node(state="root")
        self.first_child = Node(state="first",
                                parent=self.node)
        self.second_child = Node(state="second",
                                 parent=self.first_child)

    def test_get_path(self):
        test_data = [(self.second_child, [self.first_child.state, self.node.state]),
                     (self.first_child, [self.node.state]),
                     (self.node, [])]

        for n, p in test_data:
            with self.subTest("Should have returned a correct path to the root.", n=n, p=p):
                self.assertEqual(n.get_path(), p)

    def test_is_cycle(self):
        cycle_node = Node(state=self.second_child.state, parent=self.node)
        self.first_child.parent = cycle_node

        test_data = [(self.second_child, True), (self.first_child, False), (self.node, False)]

        for n, e in test_data:
            with self.subTest("Should have correctly determined if the node is part of a cycle.", n=n, e=e):
                self.assertEqual(n.is_cycle(), e)

    def test_expand(self):
        actions = {("A", 1), ("B", 1)}
        states = [a[0] for a in actions]
        expected = tuple([Node(state=a[0], parent=self.node, action=a, path_cost=a[1]) for a in actions])

        mock_problem = Mock(spec_set=Problem)
        mock_problem.get_actions.return_value = actions
        mock_problem.apply_action.side_effect = states

        self.assertEqual(tuple(self.node.expand(mock_problem)), expected)