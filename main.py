import sys
from typing import List
from src.parser.map_parser import map_parsing, MapError, Map
from src.models.graph import Graph
from src.simulation.engine import create_drones, run_simulation
from src.visualization.renderer import PygameVisualizer
from src.models.drone import Drone


def main() -> None:
    """the main function that runs the program"""
    if len(sys.argv) > 1:
        map_path: str = sys.argv[1]
    else:
        print("Error: Please provide a map path.")
        sys.exit(1)
    try:
        my_map: Map = map_parsing(map_path)
    except MapError as e:
        print(f"Error: {e}")
        sys.exit(1)
    graph: Graph = Graph(my_map)
    graph.get_zones()
    graph.get_neighbors()
    drones: List[Drone] = create_drones(graph)
    visualizer: PygameVisualizer = PygameVisualizer(graph)
    print("Starting simulation...")
    total_turns: int = run_simulation(graph, drones, visualizer)
    print(f"\nSuccess! All drones arrived in {total_turns} turns.")
    while True:
        visualizer.check_events()


if __name__ == "__main__":
    main()
