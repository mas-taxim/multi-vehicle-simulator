from datetime import datetime

from object.Location import Location


class Task:
    def __init__(self, idx: int, loc: Location, create_time: datetime, elapsed_time: int):
        self.idx: int = idx
        self.loc: Location = loc
        self.create_time: datetime = create_time
        self.elapsed_time: int = elapsed_time
