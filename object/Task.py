from datetime import datetime

from object.Location import Location


class Task:
    WAIT: int = 0
    ALLOC: int = 1
    MOVING: int = 2
    ARRIVE: int = 3
    WORK: int = 4
    DONE: int = 5

    def __init__(self, idx: int, loc: Location, create_time: datetime, elapsed_time: int):
        self.idx: int = idx
        self.loc: Location = loc
        self.create_time: datetime = create_time
        self.elapsed_time: int = elapsed_time

        self.end_time: datetime = None
        self.status: int = Task.WAIT
