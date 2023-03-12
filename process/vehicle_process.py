import logging
import math
from datetime import datetime, timedelta

from object.Path import Path
from object.Location import is_same_location
from object.Vehicle import Vehicle
from object.VehicleMgr import VehicleMgr
from object.Task import Task

logger = logging.getLogger("main")


def vehicle_process(n_time: datetime, vehicle_mgr: VehicleMgr):
    for v_name in vehicle_mgr.vehicles:
        vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)
        task: Task = vehicle_mgr.get_alloced_task(v_name)

        if vehicle.status == Vehicle.WAIT:
            pass
        elif vehicle.status == Vehicle.ALLOC:
            alloc(n_time, vehicle, task)
        elif vehicle.status == Vehicle.MOVE_TO_LOAD:
            move_to_load(n_time, vehicle, task)
        elif vehicle.status == Vehicle.LOAD_START:
            load_start(n_time, vehicle, task)
        elif vehicle.status == Vehicle.LOADING:
            loading(n_time, vehicle, task)
        elif vehicle.status == Vehicle.LOAD_END:
            load_end(n_time, vehicle, task)
        elif vehicle.status == Vehicle.MOVE_TO_UNLOAD:
            move_to_unload(n_time, vehicle, task)
        elif vehicle.status == Vehicle.UNLOAD_START:
            unload_start(n_time, vehicle, task)
        elif vehicle.status == Vehicle.UNLOADING:
            unloading(n_time, vehicle, task)
        elif vehicle.status == Vehicle.UNLOAD_END:
            unload_end(n_time, vehicle, task)
        else:
            logger.error(
                f"[vehicle_process] Exception occurred in the status of vehicle -> name:{vehicle.name}, status:{vehicle.status}")


def move(vehicle: Vehicle, path: Path = None):
    '''
    걸리는 시간이 dest 와 arrive의 Euclidean distance로 계산되고 있음.
    move time 정의 -> dest 와 arrive Euclidean distance * weight 값으로 표현
    '''
    if path is None:
        if vehicle.route:
            path = vehicle.route[0]
        else:
            logger.error(f"[move] vehicle's route is empty -> name:{vehicle.name}")

    point = path.arrive_loc

    unit_length = 0.01
    length = math.sqrt((point.x - vehicle.loc.x) ** 2 + (point.y - vehicle.loc.y) ** 2) * path.weight

    if length < unit_length:
        vehicle.loc.x = point.x
        vehicle.loc.y = point.y
    else:
        vehicle.loc.x += (point.x - vehicle.loc.x) / length * unit_length
        vehicle.loc.y += (point.y - vehicle.loc.y) / length * unit_length

    if is_same_location(vehicle.loc, point) and len(vehicle.route) > 1:
        vehicle.route.pop(0)


def alloc(n_time: datetime, vehicle: Vehicle, task: Task):
    vehicle.status = Vehicle.MOVE_TO_LOAD
    task.status = Task.MOVE_TO_LOAD


def move_to_load(n_time: datetime, vehicle: Vehicle, task: Task):
    if not is_same_location(vehicle.loc, task.loc_load):
        move(vehicle)
    else:
        vehicle.status = Vehicle.LOAD_START
        task.status = Task.LOAD_START

        task.load_start_time = n_time


def load_start(n_time: datetime, vehicle: Vehicle, task: Task):
    vehicle.status = Vehicle.LOADING
    task.status = Task.LOADING


def loading(n_time: datetime, vehicle: Vehicle, task: Task):
    if task.load_start_time + timedelta(minutes=task.elapsed_time) >= n_time:
        pass
    else:
        vehicle.status = vehicle.LOAD_END
        task.status = Task.LOAD_END

        task.load_end_time = n_time


def load_end(n_time: datetime, vehicle: Vehicle, task: Task):
    vehicle.status = Vehicle.MOVE_TO_UNLOAD
    task.status = Task.MOVE_TO_UNLOAD


def move_to_unload(n_time: datetime, vehicle: Vehicle, task: Task):
    if not is_same_location(vehicle.loc, task.loc_unload):
        move(vehicle)
    else:
        vehicle.status = Vehicle.UNLOAD_START
        task.status = Task.UNLOAD_START
        task.unload_start_time = n_time


def unload_start(n_time: datetime, vehicle: Vehicle, task: Task):
    vehicle.status = Vehicle.UNLOADING
    task.status = Task.UNLOADING


def unloading(n_time: datetime, vehicle: Vehicle, task: Task):
    if task.unload_start_time + timedelta(minutes=task.elapsed_time) >= n_time:
        pass
    else:
        vehicle.status = Vehicle.UNLOAD_END
        task.status = Task.UNLOAD_END
        task.unload_end_time = n_time


def unload_end(n_time: datetime, vehicle: Vehicle, task: Task):
    vehicle.status = Vehicle.WAIT
    vehicle.route = []
