from object.Vehicle import Vehicle
from object.Task import Task
from object.VehicleMgr import VehicleMgr
from object.TaskMgr import TaskMgr


def allocate(vehicle_mgr: VehicleMgr, task_mgr: TaskMgr, v_name: str, t_idx: int):
    vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)
    task: Task = task_mgr.get_task(t_idx)

    vehicle_mgr.alloc_task(v_name, task)
    task_mgr.alloc_vehicle(t_idx, vehicle)

    vehicle.status = Vehicle.ALLOC
    vehicle.dest = task.loc
