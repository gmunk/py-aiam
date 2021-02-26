from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True, eq=True)
class VacuumPerception:
    location: str = None
    status: str = None


AgentProgram = Callable[[Any], str]
ParsePerception = Callable[[Any], Any]
Rules = dict[Any, str]
MatchRule = Callable[[Any, Rules], str]


def create_table_driven_agent_program(table: dict[tuple, str]) -> AgentProgram:
    """Creates an implementation of a table-driven agent program.

    Parameters
    ----------
    table : dict[tuple, str]
        Dictionary of tuple to action description mappings. The tuples represent perception sequences.

    Returns
    -------
    Callable[[Any], str]
        Callable implementation of a table-driven agent program.
    """
    perception_sequence = []

    def execute(perception: Any) -> str:
        """Executes the table-driven agent program.

        Uses a tuple representation of the persistent perception sequence to reference a table of mappings.

        Parameters
        ----------
        perception : Any
            Representation of a perception.

        Returns
        -------
        str
            Description of an action.
        """
        perception_sequence.append(perception)

        return table.get(tuple(perception_sequence))

    return execute


def create_reflex_vacuum_agent_program() -> AgentProgram:
    """Creates reflex agent, mimicking a vacuum cleaner.

    Returns
    -------
    Callable[[Any], str]
        Callable implementation of a reflex vacuum agent program.
    """

    def execute(perception: Any) -> str:
        """Executes the reflex vacuum agent program.

        Parameters
        ----------
        perception : Any
            Representation of a perception.

        Returns
        -------
        str
            Description of an action.
        """
        return "Suck" if perception.status == "Dirty" \
            else "Right" if perception.location == "A" \
            else "Left" if perception.location == "B" \
            else None

    return execute


def parse_vacuum_perception(perception: VacuumPerception) -> str:
    """Parses a vacuum agent's perception of the current state of the vacuum world.

    Parameters
    ----------
    perception : VacuumPerception
        Perception of the vacuum world. Includes a location and its status.

    Returns
    -------
    str
        Description of the current state of the vacuum world. Used to feed a condition-action mechanism.
    """
    return "Is {}".format(perception.status) if perception.status == "Dirty"\
        else "Is Clean {}".format(perception.location)


def match_vacuum_rule(state: Any, rules: Rules) -> str:
    """Matches a state to an action in the vacuum world where a simple reflex vacuum agent will work.

    Parameters
    ----------
    state : Any
        Vacuum world state.
    rules : dict[Any, str]
        Condition-action rules for the vacuum world.

    Returns
    -------
    str
        Action which the simple reflex vacuum agent should take next.
    """
    return rules.get(state)


def create_simple_reflex_agent(rules: Rules, parse_perception: ParsePerception, match_rule: MatchRule) -> AgentProgram:
    """Creates a generalized reflex agent based on condition-action rules.

    Parameters
    ----------
    rules : dict[Any, str]
        Mapping of rules, it provides an appropriate action for each valid state the agent might be in.
    parse_perception : Callable[[Any], Any]
        Callable that parses a perception and returns a description of a state.
    match_rule : Callable[[Any, Rules], str]
        Function that matches a state description to an action.

    Returns
    -------
    Callable[[Any], str]
        Callable implementation of a generalized reflex agent program.
    """
    def execute(perception: Any) -> str:
        """Executes the generalized reflex agent program.

        Parameters
        ----------
        perception : Any
            Representation of a perception.

        Returns
        -------
        str
            Description of an action.
        """
        return match_rule(parse_perception(perception), rules)

    return execute
