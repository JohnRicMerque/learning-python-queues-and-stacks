import networkx as nx
import os
os.add_dll_directory("C:/Program Files/Graphviz/bin") # adding my directory path for graphviz to fix import module error on my pc
from typing import NamedTuple
from queues import Queue, Stack
from collections import deque
from math import inf as infinity
from queues import MutableMinHeap, Queue, Stack

class City(NamedTuple):
    name: str
    country: str
    year: int | None
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, attrs):
        return cls(
            name=attrs["xlabel"],
            country=attrs["country"],
            year=int(attrs["year"]) or None,
            latitude=float(attrs["latitude"]),
            longitude=float(attrs["longitude"]),
        )
    
def load_graph(filename, node_factory):
    graph = nx.nx_agraph.read_dot(filename)
    nodes = {
        name: node_factory(attributes)
        for name, attributes in graph.nodes(data=True)
    }

    return nodes, nx.Graph(
        (nodes[name1], nodes[name2], weights)
        for name1, name2, weights in graph.edges(data=True)
    )

def sort_by(neighbors, strategy):
    return sorted(neighbors.items(), key=lambda item: strategy(item[1]))

def by_distance(weights):
    return float(weights["distance"])

def is_twentieth_century(year):
    return year and 1901 <= year <= 2000

def is_twentieth_century(city):
    return city.year and 1901 <= city.year <= 2000

def order(neighbors):
    def by_latitude(city):
        return city.latitude
    return iter(sorted(neighbors, key=by_latitude, reverse=True))

def breadth_first_traverse(graph, source):
    queue = Queue(source)
    visited = {source}
    while queue:
        yield (node := queue.dequeue())
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

def breadth_first_search(graph, source, predicate, order_by=None):
    return search(breadth_first_traverse, graph, source, predicate, order_by)

def shortest_path(graph, source, destination, order_by=None):
    queue = Queue(source)
    visited = {source}
    previous = {}
    while queue:
        node = queue.dequeue()
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
                previous[neighbor] = node
                if neighbor == destination:
                    return retrace(previous, source, destination)

def retrace(previous, source, destination):
    path = deque()

    current = destination
    while current != source:
        path.appendleft(current)
        current = previous.get(current)
        if current is None:
            return None

    path.appendleft(source)
    return list(path)

def by_latitude(city):
    return -city.latitude

def connected(graph, source, destination):
    return shortest_path(graph, source, destination) is not None

def depth_first_traverse(graph, source, order_by=None):
    stack = Stack(source)
    visited = set()
    while stack:
        if (node := stack.dequeue()) not in visited:
            yield node
            visited.add(node)
            neighbors = list(graph.neighbors(node))
            if order_by:
                neighbors.sort(key=order_by)
            for neighbor in reversed(neighbors):
                stack.enqueue(neighbor)

def recursive_depth_first_traverse(graph, source, order_by=None):
    visited = set()

    def visit(node):
        yield node
        visited.add(node)
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                yield from visit(neighbor)

    return visit(source)

def depth_first_search(graph, source, predicate, order_by=None):
    return search(depth_first_traverse, graph, source, predicate, order_by)

def search(traverse, graph, source, predicate, order_by=None):
    for node in traverse(graph, source, order_by):
        if predicate(node):
            return node

def dijkstra_shortest_path(graph, source, destination, weight_factory):
    previous = {}
    visited = set()

    unvisited = MutableMinHeap()
    for node in graph.nodes:
        unvisited[node] = infinity
    unvisited[source] = 0

    while unvisited:
        visited.add(node := unvisited.dequeue())
        for neighbor, weights in graph[node].items():
            if neighbor not in visited:
                weight = weight_factory(weights)
                new_distance = unvisited[node] + weight
                if new_distance < unvisited[neighbor]:
                    unvisited[neighbor] = new_distance
                    previous[neighbor] = node

    return retrace(previous, source, destination)

def distance(weights):
    return float(weights["distance"])

def weight(node1, node2, weights):
    return distance(weights)

nodes, graph = load_graph("roadmap.dot", City.from_dict)



# TEST SCRIPTS


# READING DOT FILE TEST
# graph = nx.nx_agraph.read_dot("roadmap.dot")
# print(graph.nodes["london"])


# GRAPH INSTANTIATION AND NODE IDENTIFIERS TEST
# nodes, graph = load_graph("roadmap.dot", City.from_dict)
# print(nodes["london"])
# print(graph)


# NEIGHBORS IDENTIFIERS TEST
# for neighbor in graph.neighbors(nodes["london"]):
#     print(neighbor.name)


# NEIGHBORS WITH NODE WEIGHTS TEST 
# for neighbor, weights in graph[nodes["london"]].items():
#     print(weights["distance"], neighbor.name)


# SORTED NEIGHBORS WITH NODE WEIGHTS TEST
# for neighbor, weights in sort_by(graph[nodes["london"]], by_distance):
#     print(f"{weights['distance']:>3} miles, {neighbor.name}")


# BREADTH FIRST SEARCH FOR 20TH CENTURY CITY TEST
# for node in nx.bfs_tree(graph, nodes["edinburgh"]):
#     print("????", node.name)
#     if is_twentieth_century(node.year):
#         print("Found:", node.name, node.year)
#         break
#     else:
#         print("Not found")


# BREADTH FIRST SEARCH FOR 20TH CENTURY CITY STARTING WITH HIGHER LATITUDE TEST 
# for node in nx.bfs_tree(graph, nodes["edinburgh"], sort_neighbors=order):
#     print("????", node.name)
#     if is_twentieth_century(node.year):
#         print("Found:", node.name, node.year)
#         break
#     else:
#         print("Not found")


# USING CUSTOM MADE BREADTH FIRST SEARCH FUNCTION TEST
# for city in breadth_first_traverse(graph, nodes["edinburgh"]):
#     print(city.name)


# SHORTEST PATH USING BREADTH FIRST TRAVERSAL TEST
# city1 = nodes["aberdeen"]
# city2 = nodes["perth"]

# for i, path in enumerate(nx.all_shortest_paths(graph, city1, city2), 1):
#     print(f"{i}.", " ??? ".join(city.name for city in path))


# SHORTEST PATH NATURAL ORDER OF NEIGHBORS TEST
# city1 = nodes["aberdeen"]
# city2 = nodes["perth"]
# print(" ??? ".join(city.name for city in shortest_path(graph, city1, city2)))


# SHORTEST PATH WITH PREFERENCE TO NEIGHBORS OF HIGHER LATITUDE TEST
# print(" ??? ".join(city.name for city in shortest_path(graph, city1, city2, by_latitude)))


# CONNECTED FUNCTION TEST
# print(connected(graph, nodes["belfast"], nodes["glasgow"]))
# print(connected(graph, nodes["belfast"], nodes["derry"]))


# DEPTH-FIRST SEARCH USING A LIFO QUEUE 
# for node in nx.dfs_tree(graph, nodes["edinburgh"]):
#     print("????", node.name)
#     if is_twentieth_century(node.year):
#         print("Found:", node.name, node.year)
#         break
#     else:
#         print("Not found")

# MODIFIED BREADTH FIRST SEARCH AND DEPTH FIRST SEARCH TEST
# for city in depth_first_traverse(graph, nodes["edinburgh"]):
#     print(city.name)

# from graph import depth_first_search as dfs
# city = dfs(graph, nodes["edinburgh"], is_twentieth_century)
# print(city.name)

# TESTING DIJKSTRA???S ALGORITHM
city1 = nodes["london"]
city2 = nodes["edinburgh"]

for city in dijkstra_shortest_path(graph, city1, city2, distance):
    print(city.name)

for city in nx.dijkstra_path(graph, city1, city2, weight):
    print(city.name)