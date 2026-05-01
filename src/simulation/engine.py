import sys
from src.models.drone import Drone
from src.pathfinding.algorithm import find_all, assign_path
import pygame


def create_drones(graph):
    drone_path = assign_path(graph, find_all(graph))
    # drone_depart = each_turn(drone_path)
    drones = []
    for drone, path in drone_path.items():
        # depart = drone_depart[drone]
        drone = Drone(drone, path)
        drones.append(drone)
    return drones


def get_next_zone(drone):
    if drone.step + 1 >= len(drone.path):
        return None
    return drone.path[drone.step + 1]


def is_zone_available(zone_name, drones, graph):
    if zone_name == graph.start.name or zone_name == graph.end.name:
        return True
    zone = graph.zones[zone_name]
    occ_nb = sum(
        1 for d in drones
        if d.current_zone == zone_name and not d.in_transit
    )
    inc_nb = sum(
        1 for d in drones
        if d.in_transit and get_next_zone(d) == zone_name
    )
    return occ_nb + inc_nb < zone.max_drones


def is_connection(z1, z2, graph, usage):
    nb_c = 1
    for c in graph.map.connections:
        # Guarantee it checks both connection flows
        # exactly matching the parsed text:
        if ((z1 == c.zone1 and z2 == c.zone2)
                or (z1 == c.zone2 and z2 == c.zone1)):
            nb_c = c.max_link_capacity
            break

    conn_name = tuple(sorted([z1, z2]))
    in_use = usage.get(conn_name, 0)
    return in_use < nb_c
# def is_connection(z1, z2, graph, usage):
#     nb_c = 1
#     for c in graph.map.connections:
#         if (z1 == c.zone1 and z2 == c.zone2) or \
#             nb_c = c.max_link_capacity
#             break
#     conn_name = tuple(sorted([z1, z2]))
#     in_use = usage.get(conn_name, 0)
#     return in_use < nb_c


def visualizing(visualizer, turn, drones):
    visualizer.draw_turn(turn, drones)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False


def run_simulation(graph, drones, visualizer=None):
    turn = 0
    while not all(d.arrived for d in drones):
        if visualizer:
            visualizing(visualizer, turn, drones)
        turn_output = []
        usage = {}
        just_arrived = set()
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
            current_z_name = d.current_zone
            next_z_name = get_next_zone(d)
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
                conn_name = tuple(sorted([current_z_name, next_z_name]))
                usage[conn_name] = usage.get(conn_name, 0) + 1
                turn_output.append(f"{d.id}-{next_z_name}")
        if turn_output:
            print(" ".join(turn_output))

        turn += 1
    visualizing(visualizer, turn, drones)
    return turn
