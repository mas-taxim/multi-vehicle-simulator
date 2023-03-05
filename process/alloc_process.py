import logging
import datetime

from object.Vehicle import Vehicle
from object.VehicleMgr import VehicleMgr
from object.Task import Task
from object.TaskMgr import TaskMgr

from allocator.vehicle_allocator import allocate

logger = logging.getLogger("main")


def alloc_process(n_time: datetime, graph_name: str, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    if not task_mgr.is_remain_wait_task():
        logger.info(f"[alloc_process] : Task to assign does not exist")
        return [None, None]

    task: Task = task_mgr.peek_wait_task()

    for v_name in vehicle_mgr.vehicles:
        vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)
        if vehicle.status == Vehicle.WAIT:
            allocate(n_time, graph_name, vehicle_mgr, task_mgr, v_name, task.idx)
            task_mgr.poll_wait_task()
            logger.info(f"[alloc_process] : {task.idx} is allocated to {v_name}")
            return [v_name, task.idx]

    logger.info(f"[alloc_process] : Vehicle to be allocated does not exist")
    return [None, None]
