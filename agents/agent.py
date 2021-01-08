from abc import ABC, abstractmethod
from enum import Enum
from .exceptions import TableDrivenAgentError


class Agent(ABC):
    @abstractmethod
    def execute(self, perception):
        pass


class TableDrivenAgentPerceptions(Enum):
    PERCEPTION_SEQ_1 = "1"
    PERCEPTION_SEQ_2 = "1, 2"
    PERCEPTION_SEQ_3 = "1, 2, 3"


class TableDrivenAgentActions(Enum):
    ACTION_1 = 1
    ACTION_2 = 2
    ACTION_3 = 3


class TableDrivenAgent(Agent):
    ACTIONS = {TableDrivenAgentPerceptions.PERCEPTION_SEQ_1.value: TableDrivenAgentActions.ACTION_1,
               TableDrivenAgentPerceptions.PERCEPTION_SEQ_2.value: TableDrivenAgentActions.ACTION_2,
               TableDrivenAgentPerceptions.PERCEPTION_SEQ_3.value: TableDrivenAgentActions.ACTION_3}

    def __init__(self):
        self.perception_sequence = []

    def execute(self, perception):
        self.perception_sequence.append(perception)
        return self.__lookup()

    def __lookup(self):
        ps = ", ".join(map(str, self.perception_sequence))
        if ps not in self.ACTIONS:
            raise TableDrivenAgentError(
                "Actions lookup table for this agents does not contain an entry for the supplied perception sequence")

        return self.ACTIONS[ps]
