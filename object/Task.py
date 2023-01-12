from datetime import datetime

from object.Location import Location


class Task:
    WAIT: int = 0
    ALLOC: int = 1
    MOVING: int = 2
    ARRIVE: int = 3
    WORKING: int = 4
    DONE: int = 5

    def __init__(self, idx: int, loc: Location, create_time: datetime, elapsed_time: int):
        self.idx: int = idx
        self.loc: Location = loc
        self.elapsed_time: int = elapsed_time
        self.create_time: datetime = create_time
        self.alloc_time: datetime = None
        self.move_time: datetime = None
        self.arrive_time: datetime = None
        self.work_time: datetime = None
        self.done_time: datetime = None
        self.status: int = Task.WAIT

    def get_log(self):
        log = dict()

        log["idx"] = self.idx
        log["loc"] = str(self.loc)
        log["elapsed_time"] = self.elapsed_time
        log["create_time"] = self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time is not None else None
        log["alloc_time"] = self.alloc_time.strftime("%Y-%m-%d %H:%M:%S") if self.alloc_time is not None else None
        log["move_time"] = self.move_time.strftime("%Y-%m-%d %H:%M:%S") if self.move_time is not None else None
        log["arrive_time"] = self.arrive_time.strftime("%Y-%m-%d %H:%M:%S") if self.arrive_time is not None else None
        log["work_time"] = self.work_time.strftime("%Y-%m-%d %H:%M:%S") if self.work_time is not None else None
        log["done_time"] = self.done_time.strftime("%Y-%m-%d %H:%M:%S") if self.done_time is not None else None
        log["status"] = self.status

        return log
