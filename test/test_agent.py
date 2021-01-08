import unittest
from collections import namedtuple
from agents.agent import TableDrivenAgentActions, TableDrivenAgent
from agents.reflex_agent import ReflexVacuumAgentStates, ReflexVacuumAgentLocations, ReflexVacuumAgentActions, \
    ReflexVacuumAgent
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
        Perception = namedtuple("Perception", ["state", "location"])

        test_data = [
            (Perception(ReflexVacuumAgentStates.DIRTY, ReflexVacuumAgentLocations.A), ReflexVacuumAgentActions.SUCK),
            (Perception(ReflexVacuumAgentStates.CLEAN, ReflexVacuumAgentLocations.A), ReflexVacuumAgentActions.RIGHT),
            (Perception(ReflexVacuumAgentStates.DIRTY, ReflexVacuumAgentLocations.B), ReflexVacuumAgentActions.SUCK),
            (Perception(ReflexVacuumAgentStates.CLEAN, ReflexVacuumAgentLocations.B), ReflexVacuumAgentActions.LEFT)]

        agent = ReflexVacuumAgent()

        for p, a in test_data:
            with self.subTest(p=p, a=a):
                self.assertEqual(agent.execute(p), a)

        with self.subTest():
            self.assertRaises(ReflexVacuumAgentLocationError, agent.execute, Perception("Dirty", "C"))
