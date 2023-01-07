from object.Vehicle import Vehicle
from object.Task import Task


class VehicleMgr:
    def __init__(self):
        self.vehicles: dict[str, Vehicle] = dict()
        self.tasks_alloced: dict[str, Task] = dict()
