from object.Location import Location


class Path:
    def __init__(self, depart_loc: Location = None, arrive_loc: Location = None, weight: int = 1):
        self.depart_loc: Location = depart_loc
        self.arrive_loc: Location = arrive_loc
        self.weight: int = weight

    def __str__(self):
        return f"x: {self.arrive_loc.x}, y: {self.arrive_loc.y}"
