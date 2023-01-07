import logging

from queue import PriorityQueue
from datetime import datetime

from object.Location import Location
from object.Task import Task
from object.Vehicle import Vehicle

logger = logging.getLogger("main")


class TaskMgr:
    def __init__(self):
        self.tasks: dict[int, Task] = dict()
        self.queue: PriorityQueue[Task] = PriorityQueue()
        self.vehicles_alloced: dict[int, Vehicle] = dict()

    def get_task(self, t_idx: int):
        if t_idx in self.tasks:
            return self.tasks[t_idx]
        else:
            logger.error(f"[get_task] t_idx is not exist -> t_idx:{t_idx}")

    def add_task(self, t_idx: int, loc: Location, create_time: datetime, elapsed_time: int):
        if t_idx in self.tasks:
            logger.error(f"[add_task] t_idx exist -> t_idx:{t_idx}")
        else:
            self.tasks[t_idx] = Task(t_idx, loc, create_time, elapsed_time)
            self.queue.put(self.tasks[t_idx])
            self.vehicles_alloced[t_idx] = None

    def alloc_vehicle(self, t_idx: int, vehicle: Vehicle):
        if t_idx in self.tasks:
            self.vehicles_alloced[t_idx] = vehicle
        else:
            logger.error(f"[alloc_vehicle] t_idx is not exist -> t_idx:{t_idx}")
