from search.problem import RomanianRoadMapProblem, TreeProblem
from search.problem import Node, Action
from search.algorithms import (expand,
                               best_first_search,
                               breadth_first_search,
                               depth_first_search)
from test_problem import TestOnProblemCreatedFromFile


class TestBestFirstSearch(TestOnProblemCreatedFromFile):
    def setUp(self):
        self.problem = RomanianRoadMapProblem(states=self.states,
                                              initial_state=self.initial_state,
                                              goal_states=self.goal_states,
                                              actions=self.actions)

    def test_expand(self):
        node = Node(state="Arad")
        expected = {"Zerind", "Sibiu", "Timisoara"}

        for n in expand(self.problem, node):
            self.assertTrue(n.state in expected)

    def test_best_first_search(self):
        node = best_first_search(self.problem)
        self.assertTrue(self.problem.is_goal(node.state))


class TestBreadthFirstSearch(TestOnProblemCreatedFromFile):
    def setUp(self):
        self.problem = RomanianRoadMapProblem(states=self.states,
                                              initial_state=self.initial_state,
                                              goal_states=self.goal_states,
                                              actions=self.actions)

    def test_breadth_first_search(self):
        node = breadth_first_search(self.problem)
        self.assertTrue(self.problem.is_goal(node.state))


class TestDepthFirstSearch(TestOnProblemCreatedFromFile):
    def setUp(self):
        self.problem = TreeProblem(states={"A", "B", "C", "D", "E", "F", "G"},
                                   initial_state="A",
                                   goal_states={"M"},
                                   actions={"A": {Action(name="B"), Action(name="C")},
                                            "B": {Action(name="D"), Action(name="E")},
                                            "C": {Action(name="F"), Action(name="G")},
                                            "D": {Action(name="H"), Action(name="I")},
                                            "E": {Action(name="J"), Action(name="K")},
                                            "F": {Action(name="L"), Action(name="M")},
                                            "G": {Action(name="N"), Action(name="O")}})

    def test_depth_first_search(self):
        node = depth_first_search(self.problem)
        self.assertTrue(self.problem.is_goal(node.state))
