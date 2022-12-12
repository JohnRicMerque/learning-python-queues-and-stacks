import networkx as nx
import os
os.add_dll_directory("C:/Program Files/Graphviz/bin")

print(nx.nx_agraph.read_dot("roadmap.dot"))
