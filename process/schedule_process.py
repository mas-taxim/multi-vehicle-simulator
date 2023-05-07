import networkx as nx
from datetime import datetime, timedelta

from entity import Task, Vehicle, Location, Schedule
from graph.route import get_map
from manager import VehicleManager, TaskManager, ScheduleManager


def add_schedule(n_time: datetime, graph_name: str, vehicle: Vehicle, task: Task, schedule_mgr: ScheduleManager):
    node, node_idx, graph = get_map(graph_name)

    v_name = vehicle.name

    schedule_list = schedule_mgr.get_schedule_list(v_name)

    # load 지점까지 움직이는 schedule
    if len(schedule_list) == 0:
        start_loc: Location = Location(vehicle.loc.x, vehicle.loc.y)
        start_time: datetime = n_time
    else:
        last_schedule = schedule_list.get_last_schedule()
        start_loc: Location = Location(last_schedule.unload_loc.x, last_schedule.unload_loc.y)
        start_time: datetime = last_schedule.unload_time

    load_loc: Location = Location(task.loc_load.x, task.loc_load.y)

    move_load_time: int = nx.shortest_path_length(graph, node_idx[(start_loc.x, start_loc.y)], node_idx[(
        load_loc.x, load_loc.y)], weight='weight')

    load_time: datetime = start_time + timedelta(minutes=move_load_time + task.elapsed_time + 3)

    # unload 지점까지 움직이는 schedule
    unload_loc = Location(task.loc_unload.x, task.loc_unload.y)

    move_unload_time: int = nx.shortest_path_length(graph, node_idx[(load_loc.x, load_loc.y)], node_idx[(
        unload_loc.x, unload_loc.y)], weight='weight')

    unload_time: datetime = load_time + timedelta(minutes=move_unload_time + task.elapsed_time + 3)

    schedule_list.add_schedule(Schedule(task.idx, start_time, start_loc, load_time, load_loc, unload_time, unload_loc))


def get_earliest_vehicle(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        schedule_mgr: ScheduleManager,
        task: Task):
    node, node_idx, graph = get_map(graph_name)

    min_sched_load_time: datetime = n_time + timedelta(hours=240)
    min_vehicle: Vehicle = None

    move_unload_time = nx.shortest_path_length(graph, node_idx[(task.loc_load.x, task.loc_load.y)], node_idx[(
        task.loc_unload.x, task.loc_unload.y)], weight='weight')

    for v_name in vehicle_mgr.vehicles:
        vehicle: Vehicle = vehicle_mgr.get_vehicle(v_name)

        schedule_list = schedule_mgr.get_schedule_list(v_name)

        if len(schedule_list) == 0:
            last_sched_time = n_time
            last_loc = vehicle.loc
        else:
            last_schedule = schedule_list.get_last_schedule()
            last_sched_time = last_schedule.unload_time
            last_loc = last_schedule.unload_loc

        if vehicle.running and vehicle.close_time > last_sched_time:
            move_load_time = nx.shortest_path_length(graph, node_idx[(last_loc.x, last_loc.y)], node_idx[(
                task.loc_load.x, task.loc_load.y)], weight='weight')
            sched_load_time = last_sched_time + timedelta(minutes=move_load_time + task.elapsed_time + 3)
            sched_unload_time = sched_load_time + timedelta(minutes=move_unload_time + task.elapsed_time + 3)

            if vehicle.close_time > sched_unload_time:
                if min_sched_load_time > sched_load_time:
                    min_sched_load_time = sched_load_time
                    min_vehicle = vehicle

    return min_vehicle, min_sched_load_time


def schedule_process(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        task_mgr: TaskManager,
        schedule_mgr: ScheduleManager):
    if not task_mgr.is_remain_wait_task():
        # print("[schedule_process] : Task to schedule does not exist")
        return [None, None]

    task: Task = task_mgr.peek_wait_task()

    sched_vehicle, min_sched_load_time = get_earliest_vehicle(n_time, graph_name, vehicle_mgr, schedule_mgr, task)

    if sched_vehicle is not None:
        task_mgr.poll_wait_task()
        add_schedule(n_time, graph_name, sched_vehicle, task, schedule_mgr)
        print(f"[schedule_process] : {task.idx} is sched to {sched_vehicle.name}")
        return sched_vehicle.name, task.idx

    return [None, None]


def reschedule_process(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        task_mgr: TaskManager,
        schedule_mgr: ScheduleManager):

    # getting target task list : sched task is True, and deleted
    target_task_list = dict()
    target_tasks = schedule_mgr.clear_schedule_lists()
    if len(target_tasks) == 0:
        return
    for tid in target_tasks:
        target_task_list[tid] = True

    # looping untill all task scheduled
    batch = 1
    while len(target_task_list) > 0:
        print(f"[reschedule_process] {batch} time reschedule")
        batch += 1

        # 1. task - vehicle 쌍의 wait time 구하기
        task_vehicle_wait_time_list = []
        unsched_vehicle_list = dict()
        for task_id in target_task_list:
            task = task_mgr.get_task(task_id)
            sched_vehicle, min_sched_load_time = get_earliest_vehicle(n_time, graph_name, vehicle_mgr, schedule_mgr, task)
            wait_time = (min_sched_load_time - task_mgr.get_task(task_id).create_time).seconds
            task_vehicle_wait_time_list.append([task_id, sched_vehicle, wait_time])
            unsched_vehicle_list[sched_vehicle.name] = True

        # 2. task별 Max Wait Time을 위한 정렬
        #task_vehicle_wait_time_list = sorted(task_vehicle_wait_time_list.items(), reverse=True)
        task_vehicle_wait_time_list.sort(key=lambda x: -x[2])

        # 3. max wait time task - vehicle schedule
        for row in task_vehicle_wait_time_list:
            # row[0] : task id, row[1] : sched_vehicle, row[2] : wait_time
            task_id, sched_vehicle = row[0], row[1]
            if row[0] not in target_task_list or sched_vehicle.name not in unsched_vehicle_list:
                continue

            task = task_mgr.get_task(task_id)
            add_schedule(n_time, graph_name, sched_vehicle, task, schedule_mgr)
            print(f"[reschedule_process] : {task_id} is sched to {sched_vehicle.name}")
            del target_task_list[task_id]
            del unsched_vehicle_list[sched_vehicle.name]

    return None
