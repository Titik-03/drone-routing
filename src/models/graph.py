
from typing import Any, Dict, List
from src.parser.map_parser import Map


class Graph:
    """Graph representation of the map for pathfinding."""

    def __init__(self, map_obj: Map) -> None:
        self.zones: Dict[str, Any] = {}
        self.neighbors: Dict[str, List[Any]] = {}
        self.map: Map = map_obj
        self.start: Any = map_obj.start_hub
        self.end: Any = map_obj.end_hub
        self.nb_drones: int = map_obj.nb_drones

    def get_zones(self) -> None:
        """insert zone objects to the self.zones attribute"""

        assert self.map.start_hub is not None
        assert self.map.end_hub is not None
        self.zones[self.map.start_hub.name] = self.map.start_hub
        self.zones[self.map.end_hub.name] = self.map.end_hub
        for i in self.map.hubs:
            self.zones[i.name] = i

    def get_neighbors(self) -> None:
        """get the neighbors of each zone"""
        assert self.map.start_hub is not None
        assert self.map.end_hub is not None
        all_zones: List[Any] = (
            [self.map.start_hub, self.map.end_hub] + self.map.hubs
        )
        for i in all_zones:
            self.neighbors[i.name] = []
            for j in self.map.connections:
                if j.zone1 == i.name:
                    self.neighbors[i.name].append(self.zones[j.zone2])
                elif j.zone2 == i.name:
                    self.neighbors[i.name].append(self.zones[j.zone1])
