from typing import List


class Drone:
    """Represents a drone navigating through zones."""

    def __init__(self, id: int, path: List[str]) -> None:
        self.id: int = id
        self.path: List[str] = path
        # self.departure = departure
        self.current_zone: str = path[0]
        self.step: int = 0
        self.arrived: bool = False
        self.in_transit: bool = False
        self.waiting_turns: int = 0
