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
