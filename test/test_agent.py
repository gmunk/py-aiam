import unittest
from agents.agent import VacuumPerception, TableDrivenAgentActions, TableDrivenAgent
from agents.reflex_agent import ReflexVacuumAgentStates, ReflexVacuumAgentLocations, ReflexVacuumAgentActions, \
    ReflexVacuumAgent, SimpleReflexAgent
from agents.exceptions import TableDrivenAgentError, ReflexVacuumAgentLocationError


class TestTableDrivenAgent(unittest.TestCase):
    def test_agent_function(self):
        test_data = [(1, TableDrivenAgentActions.ACTION_1),
                     (2, TableDrivenAgentActions.ACTION_2),
                     (3, TableDrivenAgentActions.ACTION_3)]

        agent = TableDrivenAgent()

        for p, a in test_data:
            with self.subTest(p=p, a=a):
                self.assertEqual(agent.execute(p), a)

        with self.subTest():
            self.assertRaises(TableDrivenAgentError, agent.execute, "4")


class TestReflexVacuumAgent(unittest.TestCase):
    def test_agent_function(self):
        test_data = [
            (VacuumPerception(ReflexVacuumAgentStates.DIRTY, ReflexVacuumAgentLocations.A),
             ReflexVacuumAgentActions.SUCK),
            (VacuumPerception(ReflexVacuumAgentStates.CLEAN, ReflexVacuumAgentLocations.A),
             ReflexVacuumAgentActions.RIGHT),
            (VacuumPerception(ReflexVacuumAgentStates.DIRTY, ReflexVacuumAgentLocations.B),
             ReflexVacuumAgentActions.SUCK),
            (VacuumPerception(ReflexVacuumAgentStates.CLEAN, ReflexVacuumAgentLocations.B),
             ReflexVacuumAgentActions.LEFT)]

        agent = ReflexVacuumAgent()

        for p, a in test_data:
            with self.subTest(p=p, a=a):
                self.assertEqual(agent.execute(p), a)

        with self.subTest():
            self.assertRaises(ReflexVacuumAgentLocationError, agent.execute, VacuumPerception("Dirty", "C"))


class TestSimpleReflexAgent(unittest.TestCase):
    def test_agent_function(self):
        test_data = [("A", "Action A"), ("B", "Action B")]

        agent = SimpleReflexAgent(rules={
            "A": "Action A",
            "B": "Action B"
        })

        for p, a in test_data:
            with self.subTest(p=p, a=a):
                self.assertEqual(agent.execute(p), a)
