from datetime import datetime
import logging

from object.Location import Location

logger = logging.getLogger("main")


class Task:
    WAIT: int = 0
    ALLOC: int = 1
    MOVE_TO_LOAD: int = 2
    LOAD_START: int = 3
    LOADING: int = 4
    LOAD_END: int = 5
    MOVE_TO_UNLOAD: int = 6
    UNLOAD_START: int = 7
    UNLOADING: int = 8
    UNLOAD_END: int = 9

    def __init__(self, idx: int, loc_load: Location, loc_unload: Location, create_time: datetime, elapsed_time: int):
        self.idx: int = idx
        self.loc_load: Location = loc_load
        self.loc_unload: Location = loc_unload
        self.elapsed_time: int = elapsed_time
        self.create_time: datetime = create_time
        self.alloc_time: datetime = None
        self.load_start_time: datetime = None
        self.load_end_time: datetime = None
        self.unload_start_time: datetime = None
        self.unload_end_time: datetime = None
        self.status: int = Task.WAIT

    def get_log(self):
        log = dict()

        log["id"] = self.idx
        log["pick_lat"] = self.loc_load.x
        log["pick_lng"] = self.loc_load.y
        log["drop_lat"] = self.loc_unload.x
        log["drop_lng"] = self.loc_unload.y
        log["time"] = self.elapsed_time
        # log["create_time"] = self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time is not None else None
        # log["alloc_time"] = self.alloc_time.strftime("%Y-%m-%d %H:%M:%S") if self.alloc_time is not None else None
        # log["load_start_time"] = self.load_start_time.strftime(
        #     "%Y-%m-%d %H:%M:%S") if self.load_start_time is not None else None
        # log["load_end_time"] = self.load_end_time.strftime(
        #     "%Y-%m-%d %H:%M:%S") if self.load_end_time is not None else None
        # log["unload_start_time"] = self.unload_start_time.strftime(
        #     "%Y-%m-%d %H:%M:%S") if self.unload_start_time is not None else None
        # log["unload_end_time"] = self.unload_end_time.strftime(
        #     "%Y-%m-%d %H:%M:%S") if self.unload_end_time is not None else None
        log["status"] = self.status

        return log

    def get_index_log(self):
        log = dict()

        if self.status == Task.UNLOAD_END:
            log["tid"] = self.idx
            log["waittime_from_create_to_alloc"] = (self.alloc_time - self.create_time).seconds
            log["waittime_from_alloc_to_load"] = (self.load_start_time - self.alloc_time).seconds
        else:
            logger.error(f"[get_index_log] Waited task exist, tid:{self.idx}")

        return log
