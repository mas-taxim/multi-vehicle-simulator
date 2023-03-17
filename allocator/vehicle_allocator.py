import datetime

from entity.Vehicle import Vehicle
from entity.Task import Task
from entity.VehicleManager import VehicleManager
from entity.TaskManager import TaskManager

from route.route import find_graph_route


def allocate(n_time: datetime, graph_name: str, vehicle_mgr: VehicleManager, task_mgr: TaskManager, v_name: str, t_idx: int):
    vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)
    task: Task = task_mgr.get_task(t_idx)

    vehicle_mgr.alloc_task(v_name, task)
    task_mgr.alloc_vehicle(t_idx, vehicle)

    vehicle.status = Vehicle.ALLOC
    task.status = Task.ALLOC

    vehicle.dest = task.loc_unload

    # vihicle loc -> task load loc route find and alloc
    route = find_graph_route(graph_name, vehicle.loc, task.loc_load)
    vehicle.route.extend(route)

    route = find_graph_route(graph_name, task.loc_load, task.loc_unload)
    vehicle.route.extend(route)

    task.alloc_time = n_time
