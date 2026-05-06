class Connection:
    """"show a link between two zones"""

    def __init__(
        self, zone1: str, zone2: str, max_link_capacity: int = 1
    ) -> None:
        self.zone1: str = zone1
        self.zone2: str = zone2
        self.max_link_capacity: int = max_link_capacity
