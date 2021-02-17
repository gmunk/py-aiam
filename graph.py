import math
from collections import defaultdict
from typing import Sequence, Any, Optional


class Graph:
    """Implementation of a graph data structure.

    The constructor passes the connections it receives as a parameter to a private method
    which creates the internal dictionary representation of the graph.

    Attributes
    ----------
    __graph_dict : dict[Any, set[tuple[Any, float]]
        A dictionary which represents the internal state of the graph, showing the
        vertices and the edges that connect them. For example {'A': ('B', 15)} means that vertex
        A is connected to vertex B by an edge with a path-cost of 15.

    Parameters
    ----------
    connections : Sequence[tuple[Any, Any, Optional[float]]]
        A sequence of connections which are going to back this graph, an example is [('A', 'B'), ('A', 'C')].
    directed : bool
        Whether the graph is directed or undirected.
    """
    def __init__(self, connections: Sequence[tuple[Any, Any, Optional[float]]], directed: bool = False) -> None:
        self.__graph_dict = defaultdict(set)
        self.__directed = directed
        self.__create_graph_dict(connections)

    def get_vertices(self) -> set[Any]:
        """Returns the vertices in this graph.

        Based on whether the graph is directed or not, this method returns either the keys of the
        underlying dictionary combined with the first element in each edge tuple (via a set union operation) or
        just the keys of the aforementioned dictionary.

        Returns
        -------
        set[Any] :
            Set of vertices in the graph.
        """
        return set(self.__graph_dict.keys()).union(set([t[0] for v in self.__graph_dict.values() for t in v])) \
            if self.__directed else set(self.__graph_dict.keys())

    def get_edges(self, vertex: Any) -> set[tuple[Any, float]]:
        """Returns the edges originating from the provided vertex.

        Parameters
        ----------
        vertex : Any
            Vertex in the internal dictionary of the graph.

        Returns
        -------
        set[tuple[Any, float]]
            A set of the edges originating from the provided vertex or an empty set
            if the vertex is not part of the internal dictionary of the graph.
        """
        return self.__graph_dict.get(vertex, set())

    def __create_graph_dict(self, connections: Sequence[tuple[Any, Any, Optional[float]]]) -> None:
        """Creates the internal dictionary backing this implementation.

        Based on whether the graph being built is directed or not, each connection is examined
        and the necessary mappings in the dictionary data structure are created.
        For example if the method is working with the following connections [('A', 'B', 1), ('A', 'C', 1)]
        and the graph is directed, the dictionary is going to have the following connections
        {'A': ('B', 1), 'A': ('C', 1)}, if the graph is undirected this changes to
        {'A': ('B', 1), 'A': ('C', 1), 'B': ('A', 1), 'C': ('A', 1)}

        The path cost is optional, if it is not provided math.inf is used instead.

        Parameters
        ----------
        connections : Sequence[tuple[Any, Any, Optional[float]]]
            The connections which are going to back this graph, an example is [('A', 'B'), ('A', 'C')].
        """
        for first_node, second_node, *cost in connections:
            cost = cost[0] if cost else math.inf

            self.__graph_dict[first_node].add((second_node, cost))
            if not self.__directed:
                self.__graph_dict[second_node].add((first_node, cost))


romania_road_map = Graph([("Oradea", "Zerind", 71), ("Oradea", "Sibiu", 151),
                          ("Zerind", "Arad", 75),
                          ("Arad", "Sibiu", 140), ("Arad", "Timisoara", 118),
                          ("Timisoara", "Lugoj", 111),
                          ("Lugoj", "Mehadia", 70),
                          ("Mehadia", "Drobeta", 75),
                          ("Drobeta", "Craiova", 120),
                          ("Craiova", "Pitesti", 138), ("Craiova", "Rimnicu Vilcea", 146),
                          ("Rimnicu Vilcea", "Pitesti", 97),
                          ("Rimnicu Vilcea", "Sibiu", 80),
                          ("Sibiu", "Fagaras", 99),
                          ("Fagaras", "Bucharest", 211),
                          ("Pitesti", "Bucharest", 101),
                          ("Bucharest", "Giurgiu", 90), ("Bucharest", "Urziceni", 85),
                          ("Urziceni", "Vaslui", 142), ("Urziceni", "Hirsova", 98),
                          ("Vaslui", "Iasi", 92),
                          ("Iasi", "Neamt", 87),
                          ("Hirsova", "Eforie", 86)])

binary_tree = Graph([("A", "B"), ("A", "C"),
                     ("B", "D"), ("B", "E"),
                     ("C", "F"), ("C", "G"),
                     ("D", "H"), ("D", "I"),
                     ("E", "J"), ("E", "K"),
                     ("F", "L"), ("F", "M"),
                     ("G", "N"), ("G", "O")], directed=True)
