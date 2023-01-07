from queue import PriorityQueue

from object.Task import Task
from object.Vehicle import Vehicle


class TaskMgr:
    def __init__(self):
        self.tasks: dict[str, Task] = dict()
        self.queue: PriorityQueue[Task] = PriorityQueue()
        self.vehicles_alloced: dict[str, Vehicle] = dict()
