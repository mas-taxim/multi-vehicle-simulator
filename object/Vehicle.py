from object.Location import Location


class Vehicle:
    WAIT: int = 0
    ALLOC: int = 1
    MOVING: int = 2
    LOAD_START: int = 3
    LOADING: int = 4
    LOAD_END: int = 5
    UNLOAD_START: int = 6
    UNLOADING: int = 7
    UNLOAD_END: int = 8

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
        log["loc.x"] = self.loc.x
        log["loc.y"] = self.loc.y
        log["battery"] = self.battery
        log["status"] = self.status
        log["route"] = self.get_route_tuple()

        return log
