from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class VacuumPerception:
    location: str = None
    status: str = None


def create_table_driven_agent_program(table):
    """Creates an implementation of a table-driven agent program.

    Parameters
    ----------
    table : dict
        A dictionary of perception sequence to action mappings.

    Returns
    -------
    function
        A callable implementation of a table-driven agent program.
    """
    perception_sequence = []

    def execute(perception):
        """Executes the table-driven agent program.

        The function uses a tuple representation of the persistent perception sequence to reference
        a table of mappings.

        Parameters
        ----------
        perception : obj
            A representation of a perception.

        Returns
        -------
        str
            A description of an action.
        """
        perception_sequence.append(perception)

        return table.get(tuple(perception_sequence))

    return execute


def create_reflex_vacuum_agent_program():
    """Creates a specific reflex agent that mimics a vacuum cleaner.

    Returns
    -------
    function
        A callable implementation of a reflex vacuum agent program.
    """

    def execute(perception):
        """Executes the reflex vacuum agent program.

        Parameters
        ----------
        perception : obj
            A representation of a perception.

        Returns
        -------
        str
            A description of an action.
        """
        return "Suck" if perception.status == "Dirty" \
            else "Right" if perception.location == "A" \
            else "Left" if perception.location == "B" \
            else None

    return execute


def parse_vacuum_perception(perception):
    return "Is {}".format(perception.status) if perception.status == "Dirty"\
        else "Is Clean {}".format(perception.location)


def match_vacuum_rule(state, rules):
    return rules.get(state)


def create_simple_reflex_agent(rules, parse_perception, match_rule):
    """Creates a generalized reflex agent based on condition-action rules.

    Parameters
    ----------
    rules : dict
        A mapping of rules, it provides an appropriate action for each valid state the agent might be in.
    parse_perception : function
        A function that parses a perception to a description of a state.
    match_rule : function
        A function that matches a state description to an action.

    Returns
    -------
    function
        A callable implementation of a generalized reflex agent program.
    """
    def execute(perception):
        """Executes the generalized reflex agent program.

        Parameters
        ----------
        perception : dtype
            A representation of a perception.

        Returns
        -------
        str
            A description of an action.
        """
        return match_rule(parse_perception(perception), rules)

    return execute
