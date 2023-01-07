from object.Location import Location


class Vehicle:
    WAIT: int = 0
    ALLOC: int = 1
    MOVING: int = 2
    ARRIVE: int = 3
    WORK: int = 4

    def __init__(self, name):
        self.name: str = name
        self.loc: Location = Location()
        self.battery: float = 1
        self.status = Vehicle.WAIT
        self.dest: Location = None
        self.route: list[Location] = []
