import math
from collections import defaultdict


class Graph:
    def __init__(self, connections, directed=False):
        self.__graph_dict = defaultdict(set)
        self.__directed = directed
        self.__create_graph_dict(connections)

    def get_nodes(self):
        return set(self.__graph_dict.keys()).union(set([t[0] for v in self.__graph_dict.values() for t in v]))

    def get_connections(self, node):
        return self.__graph_dict.get(node, set())

    def __create_graph_dict(self, connections):
        for first_node, second_node, *cost in connections:
            cost = cost[0] if cost else math.inf

            self.__graph_dict[first_node].add((second_node, cost))
            if not self.__directed:
                self.__graph_dict[second_node].add((first_node, cost))
