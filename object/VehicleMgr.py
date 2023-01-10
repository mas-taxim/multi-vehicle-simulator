import logging

from object.Vehicle import Vehicle
from object.Task import Task

logger = logging.getLogger("main")


class VehicleMgr:
    def __init__(self):
        self.vehicles: dict[str, Vehicle] = dict()
        self.tasks_alloced: dict[str, Task] = dict()

    def get_vehicle(self, v_name: str):
        if v_name in self.vehicles:
            return self.vehicles[v_name]
        else:
            logger.error(f"[get_vehicle] v_name does not exist -> v_name:{v_name}")

    def add_vehicle(self, v_name: str):
        if v_name in self.vehicles:
            logger.error(f"[add_vehicle] v_name already exist -> v_name:{v_name}")
        else:
            self.vehicles[v_name] = Vehicle(v_name)
            self.tasks_alloced[v_name] = None

    def get_alloced_task(self, v_name):
        if v_name in self.vehicles:
            return self.tasks_alloced.get(v_name)
        else:
            logger.error(f"[get_vehicle] v_name does not exist -> v_name:{v_name}")
        return None

    def reset_alloced_task(self, v_name):
        self.tasks_alloced[v_name] = None

    def alloc_task(self, v_name: str, task: Task):
        if v_name in self.vehicles:
            self.tasks_alloced[v_name] = task
        else:
            logger.error(f"[get_vehicle] v_name does not exist -> v_name:{v_name}")
