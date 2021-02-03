import math
from collections import defaultdict


class Graph:
    def __init__(self, connections, directed=False):
        self.graph_dict = defaultdict(set)
        self.directed = directed
        self.__create_graph_dict(connections)

    def get_nodes(self):
        return list(self.graph_dict.keys())

    def __create_graph_dict(self, connections):
        for first_node, second_node, *cost in connections:
            cost = cost[0] if cost else math.inf

            self.graph_dict[first_node].add((second_node, cost))
            if not self.directed:
                self.graph_dict[second_node].add((first_node, cost))


romanian_road_map = [("Oradea", "Zerind", 71), ("Oradea", "Sibiu", 151),
                     ("Zerind", "Arad", 75),
                     ("Arad", "Sibiu", 140), ("Arad", "Timisoara", 118),
                     ("Timisoara", "Lugoj", 111),
                     ("Lugoj", "Mehadia", 70),
                     ("Mehadia", "Drobeta", 75),
                     ("Drobeta", "Craiova", 120),
                     ("Craiova", "Pitesti", 138), ("Craiova", "Rimnicu Vilcea", 146),
                     ("Rimnicu Vilcea", "Pitesti", 97), ("Rimnicu Vilcea", "Sibiu", 80),
                     ("Sibiu", "Fagaras", 99),
                     ("Fagaras", "Bucharest", 211),
                     ("Pitesti", "Bucharest", 101),
                     ("Bucharest", "Giurgiu", 90), ("Bucharest", "Urziceni", 85),
                     ("Urziceni", "Vaslui", 142), ("Urziceni", "Hirsova", 98),
                     ("Vaslui", "Iasi", 92),
                     ("Iasi", "Neamt", 87),
                     ("Hirsova", "Eforie", 86)]
