import logging

from datetime import datetime

from entity import Location, Task, Vehicle

logger = logging.getLogger("main")


class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = dict()
        self.wait_queue: list[int] = []
        self.vehicles_alloced: dict[int, Vehicle] = dict()
        self.task_index_log: list[dict] = []

    def get_task(self, t_idx: int):
        if t_idx in self.tasks:
            return self.tasks[t_idx]
        else:
            logger.error(f"[get_task] t_idx does not exist -> t_idx:{t_idx}")

    def add_task(self, t_idx: int, loc_load: Location, loc_unload: Location, create_time: datetime, elapsed_time: int):
        if t_idx in self.tasks:
            logger.error(f"[add_task] t_idx already exist -> t_idx:{t_idx}")
        else:
            self.tasks[t_idx] = Task(
                t_idx, loc_load, loc_unload, create_time, elapsed_time)
            self.wait_queue.append(t_idx)
            self.vehicles_alloced[t_idx] = None

    def remove_task(self, t_idx):
        if t_idx in self.tasks:
            if self.tasks.get(t_idx).status == Task.WAIT or self.tasks.get(t_idx).status == Task.LOAD_END:
                self.tasks.pop(t_idx)
                self.vehicles_alloced.pop(t_idx)

                if t_idx in self.wait_queue:
                    self.wait_queue.remove(t_idx)
            else:
                logger.error(
                    f"[remove_task] The task's status is not WAIT or DONE. -> t_idx:{t_idx}")
        else:
            logger.error(
                f"[remove_task] t_idx does not exist  -> t_idx:{t_idx}")

    def alloc_vehicle(self, t_idx: int, vehicle: Vehicle):
        if t_idx in self.tasks:
            self.vehicles_alloced[t_idx] = vehicle
        else:
            logger.error(
                f"[alloc_vehicle] t_idx does not exist -> t_idx:{t_idx}")

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

        task_logs = []

        for t_idx in self.tasks:
            task: Task = self.get_task(t_idx)
            if task.status < Task.UNLOAD_END:
                task_logs.append(task.get_log())

        return task_logs

    def get_index_log(self):

        index_logs = []

        for t_idx in self.tasks:
            task: Task = self.get_task(t_idx)
            if task.status == Task.UNLOAD_END:
                index_logs.append(task.get_index_log())

        return index_logs
