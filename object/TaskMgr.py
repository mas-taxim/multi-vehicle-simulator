from queue import PriorityQueue

from Task import Task


class TaskMgr:
    def __init__(self):
        self.tasks: dict[str, Task] = dict()
        self.queue: PriorityQueue[Task] = PriorityQueue()
