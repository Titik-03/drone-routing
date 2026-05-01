
class Graph:
    def __init__(self, map):
        self.zones = {}
        self.neighbors = {}
        self.map = map
        self.start = map.start_hub
        self.end = map.end_hub
        self.nb_drones = map.nb_drones

    def get_zones(self):
        self.zones[self.map.start_hub.name] = self.map.start_hub
        self.zones[self.map.end_hub.name] = self.map.end_hub
        for i in self.map.hubs:
            self.zones[i.name] = i

    def get_neighbors(self):
        all_zones = [self.map.start_hub, self.map.end_hub] + self.map.hubs
        for i in all_zones:
            self.neighbors[i.name] = []
            for j in self.map.connections:
                if j.zone1 == i.name:
                    self.neighbors[i.name].append(self.zones[j.zone2])
                elif j.zone2 == i.name:
                    self.neighbors[i.name].append(self.zones[j.zone1])
