class Location:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"


def is_same_location(loc1: Location, loc2: Location):
    return loc1.x == loc2.x and loc1.y == loc2.y
