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

    def get_log(self):
        log = dict()

        log["name"] = self.name
        log["loc"] = str(self.loc)
        log["battery"] = self.battery
        log["status"] = self.status
        log["route"] = self.get_route_tuple()

        return log
