from object.Location import Location


class Vehicle:
    WAIT: int = 0
    ALLOC: int = 1
    MOVING: int = 2
    ARRIVE: int = 3
    WORKING: int = 4
    DONE: int = 5

    def __init__(self, name):
        self.name: str = name
        self.loc: Location = Location()
        self.battery: float = 1
        self.status = Vehicle.WAIT
        self.route: list[Location] = []

    def get_route_tuple(self):
        route_list = []

        for r in self.route:
            route_list.append((r.x, r.y))

        return route_list
