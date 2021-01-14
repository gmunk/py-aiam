from collections import namedtuple
from abc import ABC, abstractmethod
from enum import Enum
from .exceptions import TableDrivenAgentError

VacuumPerception = namedtuple("VacuumPerception", ["state", "location"])

class Agent(ABC):
    """
    An abstract base class extended by all other agent classes.

    """

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
    """
    Implementation of an agent which works by deriving its actions from a lookup table.

    In all, but the most basic problems, modelling an agent like this is unsustainable, the table that directs the agent
    to its next action proves to be too big to compose and store. This implementation is included for the sake of
    completeness and it is only a toy.

    Attributes
    ----------
    perception_sequence : list
        A list storing the perceptions that an agent has had.
        These perceptions are then used to reference a lookup table.

    Methods
    -------
    execute(perception=1)
        Executes the agent function.
    """

    ACTIONS = {TableDrivenAgentPerceptions.PERCEPTION_SEQ_1.value: TableDrivenAgentActions.ACTION_1,
               TableDrivenAgentPerceptions.PERCEPTION_SEQ_2.value: TableDrivenAgentActions.ACTION_2,
               TableDrivenAgentPerceptions.PERCEPTION_SEQ_3.value: TableDrivenAgentActions.ACTION_3}

    def __init__(self):
        """
        Constructor for a table-driven agent.

        The constructor does not receive any parameters, the only thing it does is to initialize the agent's
        perception sequence to an empty list.
        """
        self.perception_sequence = []

    def execute(self, perception):
        """
        Implementation of this agent's agent function.

        In a table-driven agent the agent perceives its environment, appends that perception to a sequence of all
        the previous perceptions it had and with that chain it references a lookup table for its next action.

        Parameters
        ----------
        perception : Any
            The current perception of the agent.

        Returns
        -------
        str
            Description of an action which the agent should forward to its actuators.
        """
        self.perception_sequence.append(perception)
        return self.__lookup()

    def __lookup(self):
        ps = ", ".join(map(str, self.perception_sequence))
        if ps not in self.ACTIONS:
            raise TableDrivenAgentError(
                "Actions lookup table for this agents does not contain an entry for the supplied perception sequence")

        return self.ACTIONS[ps]
