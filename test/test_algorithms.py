from search.problem import Problem, RomanianRoadMapProblem
from search.problem import Node
from search.algorithms import (DEFAULT_PATH_COST,
                               expand,
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
        node = Node(state="Arad", parent=None, action=None, path_cost=DEFAULT_PATH_COST)
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
        self.problem = Problem(states={"A", "B", "C", "D", "E", "F", "G"},
                               initial_state="A",
                               goal_states={"F"},
                               actions={"A": {"B", "C"},
                                        "B": {"D", "E"},
                                        "C": {"F", "G"}})

    def test_depth_first_search(self):
        node = depth_first_search(self.problem)
        self.assertTrue(self.problem.is_goal(node.state))
