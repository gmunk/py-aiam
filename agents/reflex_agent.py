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
