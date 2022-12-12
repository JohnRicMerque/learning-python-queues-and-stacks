import networkx as nx
import os
os.add_dll_directory("C:/Program Files/Graphviz/bin")
from typing import NamedTuple

graph = nx.nx_agraph.read_dot("roadmap.dot")
graph.nodes["london"]

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
        