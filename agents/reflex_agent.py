from enum import Enum
from .agent import Agent
from .exceptions import ReflexVacuumAgentLocationError


class ReflexVacuumAgentStates(Enum):
    DIRTY = 1
    CLEAN = 2


class ReflexVacuumAgentLocations(Enum):
    A = 1
    B = 2


class ReflexVacuumAgentActions(Enum):
    SUCK = 1
    RIGHT = 2
    LEFT = 3


class ReflexVacuumAgent(Agent):
    RULES = {ReflexVacuumAgentStates.DIRTY: ReflexVacuumAgentActions.SUCK,
             ReflexVacuumAgentLocations.A: ReflexVacuumAgentActions.RIGHT,
             ReflexVacuumAgentLocations.B: ReflexVacuumAgentActions.LEFT}

    def execute(self, perception):
        if perception.location not in self.RULES:
            raise ReflexVacuumAgentLocationError(
                "This agents seems to be in an unrecognized location. This is a fatal error.")

        return self.RULES.get(perception.state, self.RULES[perception.location])


class SimpleReflexAgent(Agent):
    """
    Representation of an agent reacting to its most recent perception,
    without accounting for its whole perception history.

    Attributes
    ----------
    rules : dict
        A dictionary mapping that goes from a description of a world-state to an action.

    Methods
    -------
    execute(perception="A")
        Executes the agent function.
    """
    def __init__(self, rules=None):
        self.rules = rules if rules is not None else {}

    def execute(self, perception):
        """
        Implementation of this agent's agent function.

        The simple reflex agent uses its current perception to reference a mapping of rules, from that mapping
        it derives the next action it should execute.

        Parameters
        ----------
        perception : Any
            The current perception of the agent.

        Returns
        -------
        str
            Description of an action which the agent should forward to its actuators.
        """
        return self.__match_rule(perception)

    def __match_rule(self, state):
        return self.rules[state]
