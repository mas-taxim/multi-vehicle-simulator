import logging

from datetime import datetime

from object.Location import Location
from object.Task import Task
from object.Vehicle import Vehicle

logger = logging.getLogger("main")


class TaskMgr:
    def __init__(self):
        self.tasks: dict[int, Task] = dict()
        self.wait_queue: list[int] = []
        self.vehicles_alloced: dict[int, Vehicle] = dict()

    def get_task(self, t_idx: int):
        if t_idx in self.tasks:
            return self.tasks[t_idx]
        else:
            logger.error(f"[get_task] t_idx does not exist -> t_idx:{t_idx}")

    def add_task(self, t_idx: int, loc: Location, create_time: datetime, elapsed_time: int):
        if t_idx in self.tasks:
            logger.error(f"[add_task] t_idx already exist -> t_idx:{t_idx}")
        else:
            self.tasks[t_idx] = Task(t_idx, loc, create_time, elapsed_time)
            self.wait_queue.append(t_idx)
            self.vehicles_alloced[t_idx] = None

    def remove_task(self, t_idx):
        if t_idx in self.tasks:
            if self.tasks.get(t_idx).status == Task.WAIT or self.tasks.get(t_idx).status == Task.DONE:
                self.tasks.pop(t_idx)
                self.vehicles_alloced.pop(t_idx)

                if t_idx in self.wait_queue:
                    self.wait_queue.remove(t_idx)
            else:
                logger.error(f"[remove_task] The task's status is not WAIT or DONE. -> t_idx:{t_idx}")
        else:
            logger.error(f"[remove_task] t_idx does not exist  -> t_idx:{t_idx}")

    def alloc_vehicle(self, t_idx: int, vehicle: Vehicle):
        if t_idx in self.tasks:
            self.vehicles_alloced[t_idx] = vehicle
        else:
            logger.error(f"[alloc_vehicle] t_idx does not exist -> t_idx:{t_idx}")

    def peek_wait_task(self) -> Task:
        if self.wait_queue:
            return self.tasks.get(self.wait_queue[0])
        return None

    def poll_wait_task(self) -> Task:
        if self.wait_queue:
            return self.tasks.get(self.wait_queue.pop(0))
        return None

    def is_remain_wait_task(self):
        if self.wait_queue:
            return True
        return False

    def get_names_vehicle_alloced(self):
        name_list = []
        for t_idx in self.vehicles_alloced:
            if self.vehicles_alloced[t_idx] is None:
                name_list.append((t_idx, '-'))
            else:
                name_list.append((t_idx, self.vehicles_alloced[t_idx].name))
        return name_list

    def get_log(self):
        log = dict()

        task_log = []

        for t_idx in self.tasks:
            task: Task = self.get_task(t_idx)
            task_log.append(task.get_log())

        log['task_log'] = task_log
        log['wait_queue'] = self.wait_queue
        log['vehicles_alloced'] = self.get_names_vehicle_alloced()

        return log
