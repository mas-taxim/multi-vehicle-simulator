import datetime

from object.Vehicle import Vehicle
from object.Task import Task
from object.VehicleMgr import VehicleMgr
from object.TaskMgr import TaskMgr

from route.route import find_route


def allocate(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr, v_name: str, t_idx: int):
    vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)
    task: Task = task_mgr.get_task(t_idx)

    vehicle_mgr.alloc_task(v_name, task)
    task_mgr.alloc_vehicle(t_idx, vehicle)

    vehicle.status = Vehicle.ALLOC
    task.status = Task.ALLOC

    vehicle.dest = task.loc
    vehicle.route = find_route(vehicle.loc, task.loc)

    task.alloc_time = n_time
