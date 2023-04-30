from datetime import datetime

from .location import Location


class Schedule:
    TERMINATED: int = 0
    RUNNING: int = 1
    PLANNED: int = 2

    def __init__(self, task_id: int, start_time: datetime, start_loc: Location, load_time: datetime,
                 load_loc: Location, unload_time: datetime, unload_loc: Location):
        self.task_id: int = task_id
        self.status: int = Schedule.PLANNED
        self.start_time: datetime = start_time
        self.start_loc: Location = start_loc
        self.load_time: datetime = load_time
        self.load_loc: Location = load_loc
        self.unload_time: datetime = unload_time
        self.unload_loc: Location = unload_loc

    def set_status(self, status):
        self.status = status

    def get_log(self):
        log = dict()

        log["status"] = self.status
        log["task_id"] = self.task_id
        log["start_time"] = self.start_time.strftime("%Y-%m-%d %H:%M:%S")
        log["load_time"] = self.load_time.strftime("%Y-%m-%d %H:%M:%S")
        log["unload_time"] = self.unload_time.strftime("%Y-%m-%d %H:%M:%S")

        return log
