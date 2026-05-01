from src.models.connection import Connection
from src.models.zone import Zone

class MapError(Exception):
    pass

class Map:
    def __init__(self):
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.hubs = []
        self.connections = []


def parse_meta(meta, line_num):
    zone = "normal"
    color = None
    max_drones = 1  
    if meta == "":
        return zone, color, max_drones
    tags = meta.strip().split()
    for tag in tags:
        if tag.startswith("zone="):
            zone = tag.removeprefix("zone=")
            if zone not in ("normal", "blocked", "restricted", "priority"):
                raise MapError(f"line {line_num}: invalid zone type '{zone}'")
        elif tag.startswith("color="):
            color = tag.removeprefix("color=")
        elif tag.startswith("max_drones="):
            value = tag.removeprefix("max_drones=")
            try:
                max_drones = int(value)
            except ValueError:
                raise MapError(f"line {line_num}: max_drones value '{value}' is not a valid integer")
            if max_drones <= 0:
                raise MapError(f"line {line_num}: max_drones must be a positive integer")
        else:
            raise MapError(f"line {line_num}: unknown metadata tag '{tag}'")
    return zone, color, max_drones 


def parse_first(line, start_line, line_num):
    data = line.removeprefix(start_line)
    if "[" in data:
        if "]" not in data:
            raise MapError(f"line {line_num}: unclosed metadata bracket")
        main, meta = data.split("[", 1)
        meta = meta.rstrip("]").strip()
    else:
        main = data
        meta = ""
    parts = main.strip().split()
    if len(parts) < 3:
        raise MapError(f"line {line_num}: zone requires name, x, and y (got {len(parts)} value(s))")
    name = parts[0]
    
    if "-" in name or " " in name:
        raise MapError(f"line {line_num}: zone name cannot contain dashes or spaces")
    try:
        x = int(parts[1])
    except ValueError:
        raise MapError(f"line {line_num}: x coordinate '{parts[1]}' is not a valid integer")
    try:
        y = int(parts[2])
    except ValueError:
        raise MapError(f"line {line_num}: y coordinate '{parts[2]}' is not a valid integer")
    zone_type, color, max_drones = parse_meta(meta, line_num)
    return Zone(name, x, y, zone_type, color, max_drones)


def parse_connections(line, zone_names, line_num):
    data = line.removeprefix("connection:")
    if "[" in data:
        if "]" not in data:
            raise MapError(f"line {line_num}: unclosed metadata bracket")
        main, meta = data.split("[", 1)
        meta = meta.rstrip("]").strip()
    else:
        main = data
        meta = ""
    parts = main.strip().split("-")
    if len(parts) != 2:
        raise MapError(f"line {line_num}: connection must link exactly two zones (got '{main.strip()}')")
    zone1 = parts[0].strip()
    zone2 = parts[1].strip()
    if zone1 not in zone_names:
        raise MapError(f"line {line_num}: zone '{zone1}' is not defined")
    if zone2 not in zone_names:
        raise MapError(f"line {line_num}: zone '{zone2}' is not defined")
    if zone1 == zone2:
        raise MapError(f"line {line_num}: self-connection is not allowed ('{zone1}')")
    max_link_capacity = 1
    if meta:
        for item in meta.strip().split():
            if item.startswith("max_link_capacity="):
                value = item.removeprefix("max_link_capacity=")
                try:
                    max_link_capacity = int(value)
                except ValueError:
                    raise MapError(f"line {line_num}: max_link_capacity value '{value}' is not a valid integer")
                if max_link_capacity <= 0:
                    raise MapError(f"line {line_num}: max_link_capacity must be a positive integer")
            else:
                raise MapError(f"line {line_num}: unknown connection metadata tag '{item}'")
    return Connection(zone1, zone2, max_link_capacity)



def map_parsing(path):
    result = Map()
    zone_names = set()
    connections_seen = set()
    first_line = True
    start_count = 0
    end_count = 0
    with open(path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if first_line:
                if not line.startswith("nb_drones:"):
                    raise MapError(f"line {line_num}: first non-comment line must be 'nb_drones: <number>'")
                first_line = False
            if line.startswith("nb_drones:"):
                value = line.removeprefix("nb_drones:").strip()
                try:
                    number = int(value)
                except ValueError:
                    raise MapError(f"line {line_num}: nb_drones value '{value}' is not a valid integer")
                if number <= 0:
                    raise MapError(f"line {line_num}: nb_drones must be a positive integer")
                result.nb_drones = number
            elif line.startswith("start_hub:"):
                start_count += 1
                if start_count > 1:
                    raise MapError(f"line {line_num}: there must be only one start_hub")
                zone = parse_first(line, "start_hub:", line_num)
                if zone.name in zone_names:
                    raise MapError(f"line {line_num}: duplicate zone name '{zone.name}'")
                zone_names.add(zone.name)
                result.start_hub = zone
            elif line.startswith("end_hub:"):
                end_count += 1
                if end_count > 1:
                    raise MapError(f"line {line_num}: there must be only one end_hub")
                zone = parse_first(line, "end_hub:", line_num)
                if zone.name in zone_names:
                    raise MapError(f"line {line_num}: duplicate zone name '{zone.name}'")
                zone_names.add(zone.name)
                result.end_hub = zone
            elif line.startswith("hub:"):
                zone = parse_first(line, "hub:", line_num)
                if zone.name in zone_names:
                    raise MapError(f"line {line_num}: duplicate zone name '{zone.name}'")
                zone_names.add(zone.name)
                result.hubs.append(zone)
            elif line.startswith("connection:"):
                connection = parse_connections(line, zone_names, line_num)
                pair = frozenset({connection.zone1, connection.zone2})
                if pair in connections_seen:
                    raise MapError(f"line {line_num}: duplicate connection '{connection.zone1}-{connection.zone2}'")
                connections_seen.add(pair)
                result.connections.append(connection)
            else:
                raise MapError(f"line {line_num}: unrecognized syntax '{line}'")
    if result.start_hub is None:
        raise MapError("missing start_hub definition")
    if result.end_hub is None:
        raise MapError("missing end_hub definition")
    return result
