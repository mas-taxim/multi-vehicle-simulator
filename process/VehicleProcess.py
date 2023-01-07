from object.Vehicle import Vehicle
from object.Location import Location
from object.Task import Task


def process(vehicle: Vehicle):
    return None


def find_route(vehicle: Vehicle, dest: Location = None):
    if dest is None:
        dest = vehicle.dest

    return None


def move(vehicle: Vehicle, point: Location = None):
    if point is None:
        point = vehicle.route[0]

    return None


def execute_task(vehicle: Vehicle, task: Task = None):
    if task is None:
        task = vehicle.task

    return None
