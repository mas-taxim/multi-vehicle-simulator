from Location import Location
from Task import Task


class Vehicle:
    def __init__(self, name):
        self.name: str = name
        self.loc: Location = Location()
        self.battery: float = 1
        self.task: Task = None
        self.dest: Location = None
        self.route: list[Location] = []
