# Fly-in

A drone flight path simulation tool. It parses custom map files, finds paths through a network of zones, and simulates multiple drones flying from a start hub to an end hub while respecting zone capacities and connection limits.

## How it works

1. **Parse** a `.txt` map file that defines zones, connections, and drone count
2. **Build** a graph from the parsed map
3. **Find** all valid paths from start to end and assign them to drones
4. **Simulate** turn-by-turn movement with collision and capacity checks
5. **Visualize** the whole thing in a Pygame window

## Project structure

```
fly-in/
├── main.py                  # entry point
├── maps/                    # map files (easy, medium, hard, etc.)
├── src/
│   ├── models/
│   │   ├── zone.py          # Zone data class
│   │   ├── connection.py    # Connection between zones
│   │   ├── drone.py         # Drone state
│   │   └── graph.py         # Graph built from a parsed map
│   ├── parser/
│   │   └── map_parser.py    # map file parser + validation
│   ├── pathfinding/
│   │   └── algorithm.py     # BFS pathfinding + path assignment
│   ├── simulation/
│   │   └── engine.py        # simulation loop logic
│   └── visualization/
│       └── renderer.py      # Pygame renderer
├── Makefile
├── requirements.txt
└── README.md
```
## Explaining each file's role

* **parser/map_parser.py**: Reads the text map file and converts it into data objects, validating map rules and metadata.
    * `parse_meta`: Parses metadata tags (e.g., zone types, colors, max drones) from brackets.
    * `parse_first`: Parses base attributes for zones (name, coordinates) and calls metadata parsing.
    * `parse_connections`: Parses connection links between two zones and sets link capacities.
    * `map_parsing`: The main parsing sequence reading the map file line-by-line.
* **models/zone.py & connection.py**: Data classes representing the areas on the map and the interconnected routes between them.
* **models/drone.py**: Manages the state of an individual drone, including its assigned path and current location status.
* **models/graph.py**: Translates the parsed map data into a proper graph structure (zones and lists of neighbors) for pathfinding computation.
    * `get_zones`: Loads zone objects into an easily accessible dictionary.
    * `get_neighbors`: Identifies and maps out connected neighbors for every zone.
* **pathfinding/algorithm.py**: Explores the graph using navigation algorithms (like BFS) to assign valid routes from start to finish.
    * `find_all`: Finds all valid paths from the start hub to the end hub using a Breadth-First approach.
    * `calculate_cost`: Evaluates the cost/weight of a path based on zone types (e.g., restricted vs normal).
    * `assign_path`: Maps and assigns the best, most optimal paths among the pool of drones.
* **simulation/engine.py**: The core simulation logic that governs turn-by-turn drone traversal, enforcing capacity constraints and detecting path collisions.
    * `create_drones`: Initializes drone objects and pairs them with their calculated paths.
    * `get_next_zone`: Safely looks up the subsequent destination zone for a drone.
    * `is_zone_available`: Validates if a zone hasn't exceeded its `max_drones` threshold.
    * `is_connection`: Validates if a network link isn't exceeding its `max_link_capacity`.
    * `visualizing`: Pauses the simulation loop waiting for a user keypress (Enter) to advance the turn visually.
    * `run_simulation`: The central simulation loop that advances all drones per turn until they arrive.
* **visualization/renderer.py**: Utilizes Pygame to render the visual graph and animate drone entities moving across paths.
    * `get_color`: Resolves string color names (e.g., "red", "rainbow") into RGB tuples.
    * `check_events`: Handles Pygame window close (`pygame.QUIT`) events.
    * `draw_zone`, `draw_connection`, `draw_drone`: Primitives for rendering UI components based on coordinates.
    * `draw_turn`: Clears the screen and draws the complete network and drones for the current turn.
* **main.py**: The primary entry script.
    * `main`: Glues parsing, pathfinding, simulation, and rendering together into a single execution flow.

## Requirements

- Python 3.10+
- pygame

Install dependencies:

```bash
make install
```

Or manually:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py maps/easy/01_linear_path.txt
```

Or with the Makefile:

```bash
make run                                    # uses the default map
make run MAP=maps/medium/some_map.txt       # specify a map
```

During the simulation, press **Enter** to advance to the next turn.

## Map format

Map files are plain text. Lines starting with `#` are comments. Example:

```
nb_drones: 3
start_hub: A 0 0
end_hub: B 4 0
hub: C 2 1 [zone=restricted]
connection: A-C
connection: C-B
```

Zone metadata (optional, in brackets):
- `zone=normal|blocked|restricted|priority`
- `color=<name>`
- `max_drones=<int>`

Connection metadata (optional):
- `max_link_capacity=<int>`

## Linting

```bash
make lint          # flake8 + mypy
make lint-strict   # flake8 + mypy --strict
```

## Clean

```bash
make clean
```
