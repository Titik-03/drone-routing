import sys
from typing import List, Optional, Dict, Tuple, Any, Set
from src.models.drone import Drone
from src.models.graph import Graph
from src.pathfinding.algorithm import find_all, assign_path
import pygame


def create_drones(graph: Graph) -> List[Drone]:
    """this create the drone object"""
    drone_path: Dict[str, List[str]] = assign_path(graph, find_all(graph))
    # drone_depart = each_turn(drone_path)
    drones_list: List[Drone] = []
    for drone_id, path in drone_path.items():
        # depart = drone_depart[drone]
        drone: Drone = Drone(int(drone_id.replace("D", "")), path)
        drone.id = drone_id  # type: ignore # We use string IDs here
        drones_list.append(drone)
    return drones_list


def get_next_zone(drone: Drone) -> Optional[str]:
    """return the next zone for a drone"""
    if drone.step + 1 >= len(drone.path):
        return None
    return drone.path[drone.step + 1]


def is_zone_available(
    zone_name: str, drones: List[Drone], graph: Graph
) -> bool:
    """this checks if the next zone is full or not"""
    if zone_name == graph.start.name or zone_name == graph.end.name:
        return True
    zone = graph.zones[zone_name]
    occ_nb: int = sum(
        1 for d in drones
        if d.current_zone == zone_name and not d.in_transit
    )
    inc_nb: int = sum(
        1 for d in drones
        if d.in_transit and get_next_zone(d) == zone_name
    )
    return bool(occ_nb + inc_nb < zone.max_drones)


def is_connection(
    z1: str, z2: str, graph: Graph, usage: Dict[Tuple[str, str], int]
) -> bool:
    """this checks if the connection is full or not"""
    nb_c: int = 1
    for c in graph.map.connections:
        # Guarantee it checks both connection flows
        # exactly matching the parsed text:
        if ((z1 == c.zone1 and z2 == c.zone2)
                or (z1 == c.zone2 and z2 == c.zone1)):
            nb_c = c.max_link_capacity
            break

    # Sort it as a list, then convert to exactly two strings in a tuple
    sorted_zones = sorted([z1, z2])
    conn_name: Tuple[str, str] = (sorted_zones[0], sorted_zones[1])
    in_use: int = usage.get(conn_name, 0)
    return bool(in_use < nb_c)
# def is_connection(z1, z2, graph, usage):
#     nb_c = 1
#     for c in graph.map.connections:
#         if (z1 == c.zone1 and z2 == c.zone2) or \
#             nb_c = c.max_link_capacity
#             break
#     conn_name = tuple(sorted([z1, z2]))
#     in_use = usage.get(conn_name, 0)
#     return in_use < nb_c


def visualizing(visualizer: Any, turn: int, drones: List[Drone]) -> None:
    """this is responsible for the rendering part"""
    visualizer.draw_turn(turn, drones)
    waiting: bool = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False


def run_simulation(
    graph: Graph, drones: List[Drone], visualizer: Any = None
) -> int:
    """this is the main function that make the drones move"""
    turn: int = 0
    while not all(d.arrived for d in drones):
        if visualizer:
            visualizing(visualizer, turn, drones)
        turn_output: List[str] = []
        usage: Dict[Tuple[str, str], int] = {}
        just_arrived: Set[Any] = set()
        for d in drones:
            if d.in_transit:
                d.in_transit = False
                d.step += 1
                d.current_zone = d.path[d.step]
                just_arrived.add(d.id)
                if d.current_zone == graph.end.name:
                    d.arrived = True

        for d in drones:
            if d.in_transit or d.arrived or d.id in just_arrived:
                continue
            current_z_name: str = d.current_zone
            next_z_name: Optional[str] = get_next_zone(d)
            if not next_z_name:
                continue
            if (is_zone_available(next_z_name, drones, graph)
                    and is_connection(
                        current_z_name, next_z_name,
                        graph, usage)):
                next_zone = graph.zones[next_z_name]
                if next_zone.zone_type == "restricted":
                    d.in_transit = True
                else:
                    d.step += 1
                    d.current_zone = d.path[d.step]
                    if d.current_zone == graph.end.name:
                        d.arrived = True

                sorted_zones2 = sorted([current_z_name, next_z_name])
                conn_name_2: Tuple[str, str] = (
                    sorted_zones2[0], sorted_zones2[1]
                )

                usage[conn_name_2] = usage.get(conn_name_2, 0) + 1
                turn_output.append(f"{d.id}-{next_z_name}")
        if turn_output:
            print(" ".join(turn_output))

        turn += 1
    if visualizer:
        visualizing(visualizer, turn, drones)
    return turn
