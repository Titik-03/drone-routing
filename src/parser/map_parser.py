from typing import Tuple, List, Optional, Set, FrozenSet
from src.models.connection import Connection
from src.models.zone import Zone


class MapError(Exception):
    """raised when there is an error with the map data"""
    pass


class Map:
    """holds the parsed results"""
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.start_hub: Optional[Zone] = None
        self.end_hub: Optional[Zone] = None
        self.hubs: List[Zone] = []
        self.connections: List[Connection] = []


def parse_meta(
    meta: str, line_num: int
) -> Tuple[str, Optional[str], int]:
    """this parse the metadata of zones and connections"""
    zone: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1
    if meta == "":
        return zone, color, max_drones
    tags: List[str] = meta.strip().split()
    for tag in tags:
        if tag.startswith("zone="):
            zone = tag.removeprefix("zone=")
            if zone not in ("normal", "blocked", "restricted", "priority"):
                raise MapError(f"line {line_num}: invalid zone type '{zone}'")
        elif tag.startswith("color="):
            color = tag.removeprefix("color=")
        elif tag.startswith("max_drones="):
            value: str = tag.removeprefix("max_drones=")
            try:
                max_drones = int(value)
            except ValueError:
                raise MapError(
                    f"line {line_num}: max_drones value "
                    f"'{value}' is not a valid integer"
                )
            if max_drones <= 0:
                raise MapError(
                    f"line {line_num}: max_drones must "
                    f"be a positive integer"
                )
        else:
            raise MapError(f"line {line_num}: unknown metadata tag '{tag}'")
    return zone, color, max_drones


def parse_first(line: str, start_line: str, line_num: int) -> Zone:
    """this parse the data in each line(main data and meta data)"""
    data: str = line.removeprefix(start_line)
    if "[" in data:
        if "]" not in data:
            raise MapError(f"line {line_num}: unclosed metadata bracket")
        main, meta = data.split("[", 1)
        meta = meta.rstrip("]").strip()
    else:
        main = data
        meta = ""
    parts: List[str] = main.strip().split()
    if len(parts) < 3:
        raise MapError(
            f"line {line_num}: zone requires name, x, "
            f"and y (got {len(parts)} value(s))"
        )
    name: str = parts[0]

    if "-" in name or " " in name:
        raise MapError(
            f"line {line_num}: zone name cannot "
            f"contain dashes or spaces"
        )
    try:
        x: int = int(parts[1])
    except ValueError:
        raise MapError(
            f"line {line_num}: x coordinate "
            f"'{parts[1]}' is not a valid integer"
        )
    try:
        y: int = int(parts[2])
    except ValueError:
        raise MapError(
            f"line {line_num}: y coordinate "
            f"'{parts[2]}' is not a valid integer"
        )
    zone_type: str
    color: Optional[str]
    max_drones: int
    zone_type, color, max_drones = parse_meta(meta, line_num)
    return Zone(name, x, y, zone_type, color, max_drones)


def parse_connections(
    line: str, zone_names: Set[str], line_num: int
) -> Connection:
    """this parse the connections"""
    data: str = line.removeprefix("connection:")
    if "[" in data:
        if "]" not in data:
            raise MapError(f"line {line_num}: unclosed metadata bracket")
        main, meta = data.split("[", 1)
        meta = meta.rstrip("]").strip()
    else:
        main = data
        meta = ""
    parts: List[str] = main.strip().split("-")
    if len(parts) != 2:
        raise MapError(
            f"line {line_num}: connection must link "
            f"exactly two zones (got '{main.strip()}')"
        )
    zone1: str = parts[0].strip()
    zone2: str = parts[1].strip()
    if zone1 not in zone_names:
        raise MapError(f"line {line_num}: zone '{zone1}' is not defined")
    if zone2 not in zone_names:
        raise MapError(f"line {line_num}: zone '{zone2}' is not defined")
    if zone1 == zone2:
        raise MapError(
            f"line {line_num}: self-connection "
            f"is not allowed ('{zone1}')"
        )
    max_link_capacity: int = 1
    if meta:
        for item in meta.strip().split():
            if item.startswith("max_link_capacity="):
                value: str = item.removeprefix("max_link_capacity=")
                try:
                    max_link_capacity = int(value)
                except ValueError:
                    raise MapError(
                        f"line {line_num}: "
                        f"max_link_capacity value "
                        f"'{value}' is not a valid "
                        f"integer"
                    )
                if max_link_capacity <= 0:
                    raise MapError(
                        f"line {line_num}: "
                        f"max_link_capacity must be a "
                        f"positive integer"
                    )
            else:
                raise MapError(
                    f"line {line_num}: unknown "
                    f"connection metadata tag '{item}'"
                )
    return Connection(zone1, zone2, max_link_capacity)


def map_parsing(path: str) -> Map:
    """the main parsing function that parse the whole map"""
    result: Map = Map()
    zone_names: Set[str] = set()
    connections_seen: Set[FrozenSet[str]] = set()
    first_line: bool = True
    start_count: int = 0
    end_count: int = 0
    with open(path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if first_line:
                if not line.startswith("nb_drones:"):
                    raise MapError(
                        f"line {line_num}: first "
                        f"non-comment line must be "
                        f"'nb_drones: <number>'"
                    )
                first_line = False
            if line.startswith("nb_drones:"):
                value: str = line.removeprefix("nb_drones:").strip()
                try:
                    number: int = int(value)
                except ValueError:
                    raise MapError(
                        f"line {line_num}: nb_drones "
                        f"value '{value}' is not a "
                        f"valid integer"
                    )
                if number <= 0:
                    raise MapError(
                        f"line {line_num}: nb_drones "
                        f"must be a positive integer"
                    )
                result.nb_drones = number
            elif line.startswith("start_hub:"):
                start_count += 1
                if start_count > 1:
                    raise MapError(
                        f"line {line_num}: there must "
                        f"be only one start_hub"
                    )
                zone: Zone = parse_first(line, "start_hub:", line_num)
                if zone.name in zone_names:
                    raise MapError(
                        f"line {line_num}: duplicate "
                        f"zone name '{zone.name}'"
                    )
                zone_names.add(zone.name)
                result.start_hub = zone
            elif line.startswith("end_hub:"):
                end_count += 1
                if end_count > 1:
                    raise MapError(
                        f"line {line_num}: there must "
                        f"be only one end_hub"
                    )
                zone = parse_first(line, "end_hub:", line_num)
                if zone.name in zone_names:
                    raise MapError(
                        f"line {line_num}: duplicate "
                        f"zone name '{zone.name}'"
                    )
                zone_names.add(zone.name)
                result.end_hub = zone
            elif line.startswith("hub:"):
                zone = parse_first(line, "hub:", line_num)
                if zone.name in zone_names:
                    raise MapError(
                        f"line {line_num}: duplicate "
                        f"zone name '{zone.name}'"
                    )
                zone_names.add(zone.name)
                result.hubs.append(zone)
            elif line.startswith("connection:"):
                connection: Connection = parse_connections(
                    line, zone_names, line_num
                )
                pair: FrozenSet[str] = frozenset(
                    {connection.zone1, connection.zone2}
                )
                if pair in connections_seen:
                    raise MapError(
                        f"line {line_num}: duplicate "
                        f"connection "
                        f"'{connection.zone1}"
                        f"-{connection.zone2}'"
                    )
                connections_seen.add(pair)
                result.connections.append(connection)
            else:
                raise MapError(
                    f"line {line_num}: unrecognized "
                    f"syntax '{line}'"
                )
    if result.start_hub is None:
        raise MapError("missing start_hub definition")
    if result.end_hub is None:
        raise MapError("missing end_hub definition")
    return result
