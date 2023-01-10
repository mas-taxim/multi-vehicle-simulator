import logging
from datetime import datetime, timedelta

from object.Location import Location, is_same_location
from object.Vehicle import Vehicle
from object.VehicleMgr import VehicleMgr
from object.Task import Task

logger = logging.getLogger("main")


def vehicle_process(n_time: datetime, vehicle_mgr: VehicleMgr):
    for v_name in vehicle_mgr.vehicles:
        vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)

        if vehicle.status == Vehicle.WAIT:
            pass
        elif vehicle.status == Vehicle.ALLOC or vehicle.status == Vehicle.MOVING:
            move(n_time, vehicle_mgr, vehicle)
        elif vehicle.status == Vehicle.ARRIVE or vehicle.status == Vehicle.WORKING:
            execute_task(n_time, vehicle_mgr, vehicle)
        elif vehicle.status == Vehicle.DONE:
            re_prepare(n_time, vehicle_mgr, vehicle)
        else:
            logger.error(
                f"[vehicle_process] Exception occurred in the status of vehicle -> name:{vehicle.name}, status:{vehicle.status}")


def move(n_time: datetime, vehicle_mgr: VehicleMgr, vehicle: Vehicle, point: Location = None):
    if point is None:
        if vehicle.route:
            point = vehicle.route[0]
        else:
            logger.error(f"[move] vehicle's route is empty -> name:{vehicle.name}")

    if point.x - vehicle.loc.x != 0:
        vehicle.loc.x += int((point.x - vehicle.loc.x) / abs(point.x - vehicle.loc.x))
    if point.y - vehicle.loc.y != 0:
        vehicle.loc.y += int((point.y - vehicle.loc.y) / abs(point.y - vehicle.loc.y))

    if vehicle_mgr.get_alloced_task(vehicle.name) is not None:
        task: Task = vehicle_mgr.get_alloced_task(vehicle.name)

        if vehicle.status == Vehicle.ALLOC:
            vehicle.status = Vehicle.MOVING
            task.status = Task.MOVING
            task.move_time = n_time

        if is_same_location(vehicle.loc, point):
            if len(vehicle.route) > 1:
                vehicle.route.pop(0)
            else:
                vehicle.status = Vehicle.ARRIVE
                task.status = Task.ARRIVE
                task.arrive_time = n_time


def execute_task(n_time: datetime, vehicle_mgr: VehicleMgr, vehicle: Vehicle, task: Task = None):
    if task is None:
        task = vehicle_mgr.get_alloced_task(vehicle.name)

    if vehicle.status == Vehicle.ARRIVE:
        vehicle.status = Vehicle.WORKING
        task.status = Task.WORKING
        task.work_time = n_time

    if n_time == task.work_time + timedelta(minutes=task.elapsed_time):
        vehicle.status = Vehicle.DONE
        task.status = task.DONE
        task.done_time = n_time

        vehicle.route = []
        vehicle_mgr.reset_alloced_task(vehicle.name)

    return None


def re_prepare(n_time: datetime, vehicle_mgr: VehicleMgr, vehicle: Vehicle):
    vehicle.status = Vehicle.WAIT
