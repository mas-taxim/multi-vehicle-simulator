from datetime import datetime

from Location import Location
from Vehicle import Vehicle


class Task:
    def __init__(self, idx: int, loc: Location, create_time: datetime, elapsed_time: int):
        self.idx: int = idx
        self.loc: Location = loc
        self.create_time: datetime = create_time
        self.elapsed_time: int = elapsed_time
        self.vehicle_alloced: Vehicle = None
