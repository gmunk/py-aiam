import unittest
from agent import (VacuumPerception,
                   create_table_driven_agent_program,
                   create_reflex_vacuum_agent_program,
                   parse_vacuum_perception,
                   match_vacuum_rule,
                   create_simple_reflex_agent)


class TestTableDrivenAgentProgram(unittest.TestCase):
    def test_agent_program(self):
        p1 = VacuumPerception("A", "Clean")
        p2 = VacuumPerception("A", "Dirty")
        p3 = VacuumPerception("B", "Clean")
        p4 = VacuumPerception("B", "Dirty")

        a1, a2, a3 = "Suck", "Right", "Left"

        test_data = [(p1, a2), (p3, a3), (p2, a1), (p1, a2), (p4, a1), (p3, None)]

        agent_program = create_table_driven_agent_program({
            (p1,): a2,
            (p1, p3): a3,
            (p1, p3, p2): a1,
            (p1, p3, p2, p1): a2,
            (p1, p3, p2, p1, p4): a1,
        })

        for p, a in test_data:
            with self.subTest(p=p, a=a):
                self.assertEqual(agent_program(p), a)


class TestVacuumAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if cls is TestVacuumAgent:
            raise unittest.SkipTest("%s is an abstract base class" % cls.__name__)
        else:
            super(TestVacuumAgent, cls).setUpClass()

    def setUp(self):
        self.agent_program = None

    def test_agent_program(self):
        test_data = [(VacuumPerception("A", "Clean"), "Right"),
                     (VacuumPerception("A", "Dirty"), "Suck"),
                     (VacuumPerception("B", "Clean"), "Left"),
                     (VacuumPerception("B", "Dirty"), "Suck"),
                     (VacuumPerception("C", "Clean"), None)]

        for p, a in test_data:
            with self.subTest(p=p, a=a):
                self.assertEqual(self.agent_program(p), a)


class TestReflexVacuumAgent(TestVacuumAgent):
    def setUp(self):
        self.agent_program = create_reflex_vacuum_agent_program()


class TestSimpleReflexAgent(TestVacuumAgent):
    def setUp(self):
        self.agent_program = create_simple_reflex_agent({"Is Dirty": "Suck",
                                                         "Is Clean A": "Right",
                                                         "Is Clean B": "Left"},
                                                        parse_vacuum_perception,
                                                        match_vacuum_rule)
