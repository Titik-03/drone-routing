import sys
from src.parser.map_parser import map_parsing, MapError
from src.models.graph import Graph
from src.simulation.engine import create_drones, run_simulation
from src.visualization.renderer import PygameVisualizer

if __name__ == "__main__":

    if len(sys.argv) > 1:
        map_path = sys.argv[1]
    else:
        print("Error: Please provide a map path.")
        sys.exit(1)
    try:
        my_map = map_parsing(map_path)
    except MapError as e:
        print(f"Error: {e}")
        sys.exit(1)
    graph = Graph(my_map)
    graph.get_zones()
    graph.get_neighbors()
    drones = create_drones(graph)
    visualizer = PygameVisualizer(graph)
    print("Starting simulation...")
    total_turns = run_simulation(graph, drones, visualizer)
    print(f"\nSuccess! All drones arrived in {total_turns} turns.")
    while True:
        visualizer.check_events()
