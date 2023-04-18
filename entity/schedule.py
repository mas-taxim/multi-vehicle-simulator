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