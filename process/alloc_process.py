import logging
import datetime

from entity import Task, Vehicle
from manager import TaskManager, VehicleManager

from allocator.vehicle_allocator import allocate

logger = logging.getLogger("main")


def alloc_process(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        task_mgr: TaskManager):
    # TODO : task는 큐에서 앞에서 1개만 가져오고, vihicle은 대기중인거 아무거나 가져옴, logic 개선시 변경 필요
    if not task_mgr.is_remain_wait_task():
        logger.info("[alloc_process] : Task to assign does not exist")
        return [None, None]

    # TODO : 동시간대 wait task 중 1개만 가져올것같음, logic 개선시 변경 필요
    task: Task = task_mgr.peek_wait_task()

    for v_name in vehicle_mgr.vehicles:
        # TODO : get vegicle 가까운순서가 아닌 wait vehicle pick, logic 개선시 변경 필요
        vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)
        if vehicle.status == Vehicle.WAIT:
            allocate(n_time, graph_name, vehicle_mgr,
                     task_mgr, v_name, task.idx)
            task_mgr.poll_wait_task()
            logger.info(
                f"[alloc_process] : {task.idx} is allocated to {v_name}")
            return [v_name, task.idx]

    logger.info("[alloc_process] : Vehicle to be allocated does not exist")
    return [None, None]
