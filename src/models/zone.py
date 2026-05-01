class Zone:
    def __init__(self, name, x, y, zone_type, color, max_drones):
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
    def __repr__(self):
        return f"Zone({self.name})"