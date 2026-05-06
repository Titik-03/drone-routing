from typing import Optional


class Zone:
    """represent a zone in the map"""
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: str,
        color: Optional[str],
        max_drones: int,
    ) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: str = zone_type
        self.color: Optional[str] = color
        self.max_drones: int = max_drones

    def __repr__(self) -> str:
        return f"Zone({self.name})"
