from datetime import datetime

from .location import Location


class Schedule:

    def __init__(self, task_id: int, start_time: datetime, start_loc: Location, end_time: datetime, end_loc: Location):
        # 공차로 움직이는 경우 -1
        self.task_id: int = task_id
        self.start_time: datetime = start_time
        self.start_loc: Location = start_loc
        self.end_time: datetime = end_time
        self.end_loc: Location = end_loc

    def get_log(self):
        log = dict()

        log["task_id"] = self.task_id
        log["start_time"] = self.start_time.strftime("%Y-%m-%d %H:%M:%S")
        log["end_time"] = self.end_time.strftime("%Y-%m-%d %H:%M:%S")

        return log