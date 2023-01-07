from object.Location import Location


class Vehicle:
    WAIT: int = 0
    MOVING: int = 1
    ARRIVE: int = 2
    WORK: int = 3

    def __init__(self, name):
        self.name: str = name
        self.loc: Location = Location()
        self.battery: float = 1
        self.status = Vehicle.WAIT
        self.dest: Location = None
        self.route: list[Location] = []
