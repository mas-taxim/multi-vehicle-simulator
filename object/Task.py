from datetime import datetime

from object.Location import Location


class Task:
    WAIT: int = 0
    ALLOC: int = 1
    MOVING: int = 2
    LOAD_START: int = 3
    LOADING: int = 4
    LOAD_END: int = 5
    UNLOAD_START: int = 6
    UNLOADING: int = 7
    UNLOAD_END: int = 8

    def __init__(self, idx: int, loc: Location, create_time: datetime, elapsed_time: int):
        self.idx: int = idx
        self.loc: Location = loc
        self.elapsed_time: int = elapsed_time
        self.create_time: datetime = create_time
        self.alloc_time: datetime = None
        self.load_start_time: datetime = None
        self.load_end_time: datetime = None
        self.status: int = Task.WAIT

    def get_log(self):
        log = dict()

        log["idx"] = self.idx
        log["loc.x"] = self.loc.x
        log["loc.y"] = self.loc.y
        log["elapsed_time"] = self.elapsed_time
        log["create_time"] = self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time is not None else None
        log["alloc_time"] = self.alloc_time.strftime("%Y-%m-%d %H:%M:%S") if self.alloc_time is not None else None
        log["load_start_time"] = self.load_start_time.strftime("%Y-%m-%d %H:%M:%S") if self.load_start_time is not None else None
        log["load_end_time"] = self.load_end_time.strftime("%Y-%m-%d %H:%M:%S") if self.load_end_time is not None else None
        log["status"] = self.status

        return log
