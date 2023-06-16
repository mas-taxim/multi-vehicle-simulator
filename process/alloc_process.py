import logging
import datetime

import networkx as nx

from ..entity import Task, Vehicle, Schedule
from ..manager import TaskManager, VehicleManager, ScheduleManager

from ..allocator.vehicle_allocator import allocate

from ..graph.map import get_map

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
            # print(f"[alloc_process] : {task.idx} is allocated to {v_name}")
            return [v_name, task.idx]

    logger.info("[alloc_process] : Vehicle to be allocated does not exist")
    return [None, None]


def alloc_by_schedule(n_time: datetime, graph_name: str, vehicle_mgr: VehicleManager, task_mgr: TaskManager,
                      schedule_mgr: ScheduleManager):
    for v_name in vehicle_mgr.vehicles:
        vehicle = vehicle_mgr.get_vehicle(v_name)

        schedule_list = schedule_mgr.get_schedule_list(v_name)

        if vehicle.status == Vehicle.WAIT and len(schedule_list) > 0:
            schedule = schedule_list.get_schedule(0)
            schedule.set_status(Schedule.RUNNING)
            allocate(n_time, graph_name, vehicle_mgr, task_mgr, v_name, schedule.task_id)

            print(f"[alloc_process] : {schedule.task_id} is allocated to {v_name}")


def alloc_process_nearest(n_time: datetime, graph_name: str, vehicle_mgr: VehicleManager, task_mgr: TaskManager):
    if not task_mgr.is_remain_wait_task():
        logger.info("[alloc_process] : Task to assign does not exist")
        return [None, None]

    task: Task = task_mgr.peek_wait_task()

    nearest_vehicle = None
    min_distance = 999999999
    for v_name in vehicle_mgr.vehicles:
        vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)
        if vehicle.status == Vehicle.WAIT:
            distance = abs(vehicle.loc.x - task.loc_load.x) + \
                       abs(vehicle.loc.y - task.loc_load.y)

            if min_distance > distance:
                nearest_vehicle = vehicle
                min_distance = distance

    if nearest_vehicle is not None:
        allocate(n_time, graph_name, vehicle_mgr,
                 task_mgr, nearest_vehicle.name, task.idx)
        task_mgr.poll_wait_task()
        logger.info(
            f"[alloc_process] : {task.idx} is allocated to {nearest_vehicle.name}")
        print(f"[alloc_process] : {task.idx} is allocated to {nearest_vehicle.name}")
        return [nearest_vehicle.name, task.idx]

    logger.info("[alloc_process] : Vehicle to be allocated does not exist")
    return [None, None]


def alloc_process_min_time(n_time: datetime, graph_name: str, vehicle_mgr: VehicleManager, task_mgr: TaskManager):
    if not task_mgr.is_remain_wait_task():
        logger.info("[alloc_process] : Task to assign does not exist")
        return [None, None]

    task: Task = task_mgr.peek_wait_task()

    node, node_idx, graph = get_map(graph_name)

    nearest_vehicle = None
    min_distance = 999999999
    for v_name in vehicle_mgr.vehicles:
        vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)
        if vehicle.status == Vehicle.WAIT:
            distance = nx.shortest_path_length(graph, node_idx[(vehicle.loc.x, vehicle.loc.y)], node_idx[(
                task.loc_load.x, task.loc_load.y)], weight='weight')

            if min_distance > distance:
                nearest_vehicle = vehicle
                min_distance = distance

    if nearest_vehicle is not None:
        allocate(n_time, graph_name, vehicle_mgr,
                 task_mgr, nearest_vehicle.name, task.idx)
        task_mgr.poll_wait_task()
        logger.info(
            f"[alloc_process] : {task.idx} is allocated to {nearest_vehicle.name}")
        print(f"[alloc_process] : {task.idx} is allocated to {nearest_vehicle.name}")
        return [nearest_vehicle.name, task.idx]

    logger.info("[alloc_process] : Vehicle to be allocated does not exist")
    return [None, None]
