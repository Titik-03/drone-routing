from collections import deque
from typing import List, Dict
from src.models.graph import Graph


def find_all(graph: Graph) -> List[List[str]]:
    """this finds all paths from start to end"""
    start_name: str = graph.start.name
    end_name: str = graph.end.name
    all_paths: List[List[str]] = []
    queue: deque = deque([[start_name]])
    while queue:
        current_path: List[str] = queue.popleft()
        current: str = current_path[-1]
        if current == end_name:
            all_paths.append(current_path)
            if len(all_paths) >= 50:
                break
            continue
        for i in graph.neighbors[current]:
            if i.name in current_path:
                continue
            elif i.zone_type == "blocked":
                continue
            new_path: List[str] = list(current_path)
            new_path.append(i.name)
            queue.append(new_path)
    return all_paths


def calculate_cost(graph: Graph, path: List[str]) -> float:
    """this calculate the cost of a certain path"""
    cost: float = 0.0
    for i in path[1:]:
        zone = graph.zones[i]
        if zone.zone_type == "restricted":
            cost += 2.0
        elif zone.zone_type == "priority":
            cost += 0.5
        else:
            cost += 1.0
    return cost


def assign_path(
    graph: Graph, all_paths: List[List[str]]
) -> Dict[str, List[str]]:
    """this give each drone his own path"""
    nb: int = graph.nb_drones
    all_paths.sort(key=lambda p: calculate_cost(graph, p))
    min_cost: float = calculate_cost(graph, all_paths[0])
    average: float = min_cost * 1.38
    drone_paths: Dict[str, List[str]] = {}
    min_len: int = len(all_paths[0])
    usable: List[List[str]] = []
    for p in all_paths:
        cost: float = calculate_cost(graph, p)
        if cost > average:
            break
        if len(p) <= min_len + 1:
            usable.append(p)
    for i in range(nb):
        drone_id: str = f"D{i+1}"
        if len(all_paths) >= 2:
            drone_paths[drone_id] = usable[i % len(usable)]
        else:
            drone_paths[drone_id] = all_paths[0]
    return drone_paths

# def each_turn(drone_paths):
#     is_used = {}
#     drone_departures = {}
#     for dr, path in drone_paths.items():
#         path_key = str(path)
#         if path_key not in is_used:
#             is_used[path_key] = 0
#         drone_departures[dr] = is_used[path_key]
#         is_used[path_key] += 1
#     return drone_departures

# drone_departures = {
#     "D1": 0,
#     "D2": 0,
#     "D3": 1,
#     "D4": 1,
#     "D5": 2,
# }


# drone_paths = {
#     "D1": ["hub", "roof1", "roof2", "goal"],
#     "D2": ["hub", "corridorA", "tunnelB", "goal"],
#     "D3": ["hub", "roof1", "roof2", "goal"],
#     "D4": ["hub", "corridorA", "tunnelB", "goal"],
#     "D5": ["hub", "roof1", "roof2", "goal"],
# }
