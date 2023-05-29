from datetime import datetime, timedelta

from entity import Task, Vehicle, Location, Schedule
from graph.route import get_map, get_distance
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

    move_load_time = get_distance(graph_name, node_idx[(start_loc.x, start_loc.y)], node_idx[(load_loc.x, load_loc.y)])

    load_time: datetime = start_time + timedelta(minutes=move_load_time + task.elapsed_time + 3)

    # unload 지점까지 움직이는 schedule
    unload_loc = Location(task.loc_unload.x, task.loc_unload.y)

    move_unload_time = get_distance(graph_name, node_idx[(load_loc.x, load_loc.y)],
                                    node_idx[(unload_loc.x, unload_loc.y)])

    unload_time: datetime = load_time + timedelta(minutes=move_unload_time + task.elapsed_time + 3)

    schedule_list.add_schedule(Schedule(task.idx, task.elapsed_time, start_time, start_loc, load_time, load_loc, unload_time, unload_loc))


def get_sched_time_vehicle(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        schedule_mgr: ScheduleManager,
        task: Task):
    node, node_idx, graph = get_map(graph_name)

    sched_load_time_list = []
    vehicle_list = []

    move_unload_time = get_distance(graph_name, node_idx[(task.loc_load.x, task.loc_load.y)],
                                    node_idx[(task.loc_unload.x, task.loc_unload.y)])

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
            move_load_time = get_distance(graph_name, node_idx[(last_loc.x, last_loc.y)],
                                          node_idx[(task.loc_load.x, task.loc_load.y)])

            sched_load_time = last_sched_time + timedelta(minutes=move_load_time + task.elapsed_time + 3)
            sched_unload_time = sched_load_time + timedelta(minutes=move_unload_time + task.elapsed_time + 3)

            if vehicle.close_time > sched_unload_time:
                vehicle_list.append(vehicle)
                sched_load_time_list.append(sched_load_time)

    return vehicle_list, sched_load_time_list


def get_earliest_vehicle(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        schedule_mgr: ScheduleManager,
        task: Task):
    node, node_idx, graph = get_map(graph_name)

    min_sched_load_time: datetime = n_time + timedelta(hours=240)
    min_vehicle: Vehicle = None

    move_unload_time = get_distance(graph_name, node_idx[(task.loc_load.x, task.loc_load.y)],
                                    node_idx[(task.loc_unload.x, task.loc_unload.y)])

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
            move_load_time = get_distance(graph_name, node_idx[(last_loc.x, last_loc.y)],
                                          node_idx[(task.loc_load.x, task.loc_load.y)])

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


def swap_process(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        task_mgr: TaskManager,
        schedule_mgr: ScheduleManager):
    schedule_lists = schedule_mgr.get_schedule_lists()

    for i in range(2):
        for v_name in schedule_lists:
            print(v_name, [schedule.task_id for schedule in schedule_lists[v_name].get_schedule_list()])

        max_gain = -1
        max_info = ["-1", -1, "-1", -1]

        v_names = list(schedule_lists.keys())

        for v_idx1 in range(len(v_names)):
            v1 = v_names[v_idx1]
            for v_idx2 in range(v_idx1 + 1, len(v_names)):
                v2 = v_names[v_idx2]
                schedule_list1 = schedule_lists[v1].get_schedule_list()
                schedule_list2 = schedule_lists[v2].get_schedule_list()

                for idx1 in range(1, len(schedule_list1)):
                    for idx2 in range(1, len(schedule_list2)):
                        schedule1 = schedule_list1[idx1]
                        schedule2 = schedule_list2[idx2]

                        if schedule1.status == Schedule.PLANNED and schedule2.status == Schedule.PLANNED:
                            gain = swap_gain(graph_name, schedule_list1, idx1, schedule_list2, idx2)
                            if gain > max_gain:
                                max_gain = gain
                                max_info = [v1, idx1, v2, idx2]

        # 반복해서 swap 이 일어남
        if max_gain > 5:
            print(f"[swap] {max_gain} {max_info}")
            schedule_mgr.swap(graph_name, max_info[0], max_info[1], max_info[2], max_info[3])
        else:
            break


def swap_gain(graph_name, schedule_list1: list, idx1, schedule_list2: list, idx2):
    node, node_idx, graph = get_map(graph_name)

    schedule1 = schedule_list1[idx1]
    schedule2 = schedule_list2[idx2]

    # 기존 load time
    move_load_time_old1 = get_distance(graph_name, node_idx[schedule1.start_loc.get_tuple()],
                                       node_idx[schedule1.load_loc.get_tuple()])
    move_load_time_old2 = get_distance(graph_name, node_idx[schedule2.start_loc.get_tuple()],
                                       node_idx[schedule2.load_loc.get_tuple()])

    if len(schedule_list1) > idx1 + 1:
        next_schedule1 = schedule_list1[idx1 + 1]
        next_move_load_time_old1 = get_distance(graph_name, node_idx[schedule1.unload_loc.get_tuple()],
                                                node_idx[next_schedule1.load_loc.get_tuple()])
    else:
        next_move_load_time_old1 = 0

    if len(schedule_list2) > idx2 + 1:
        next_schedule2 = schedule_list2[idx2 + 1]
        next_move_load_time_old2 = get_distance(graph_name, node_idx[schedule2.unload_loc.get_tuple()],
                                                node_idx[next_schedule2.load_loc.get_tuple()])
    else:
        next_move_load_time_old2 = 0

    # swap 후 load time
    move_load_time_new1 = get_distance(graph_name, node_idx[schedule1.start_loc.get_tuple()],
                                       node_idx[schedule2.load_loc.get_tuple()])
    move_load_time_new2 = get_distance(graph_name, node_idx[schedule2.start_loc.get_tuple()],
                                       node_idx[schedule1.load_loc.get_tuple()])

    if len(schedule_list1) > idx1 + 1:
        next_schedule1 = schedule_list1[idx1 + 1]
        next_move_load_time_new1 = get_distance(graph_name, node_idx[schedule2.unload_loc.get_tuple()],
                                                node_idx[next_schedule1.load_loc.get_tuple()])
    else:
        next_move_load_time_new1 = 0

    if len(schedule_list2) > idx2 + 1:
        next_schedule2 = schedule_list2[idx2 + 1]
        next_move_load_time_new2 = get_distance(graph_name, node_idx[schedule1.unload_loc.get_tuple()],
                                                node_idx[next_schedule2.load_loc.get_tuple()])
    else:
        next_move_load_time_new2 = 0

    # print(schedule1.task_id, schedule2.task_id)
    # print("old : ", move_load_time_old1, move_load_time_old2, next_move_load_time_old1, next_move_load_time_old2)
    # print("new : ", move_load_time_new1, move_load_time_new2, next_move_load_time_new1, next_move_load_time_new2)

    old_time = move_load_time_old1 + move_load_time_old2 + next_move_load_time_old1 + next_move_load_time_old2
    new_time = move_load_time_new1 + move_load_time_new2 + next_move_load_time_new1 + next_move_load_time_new2

    return old_time - new_time


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

            sched_vehicle, min_sched_load_time = get_earliest_vehicle(n_time, graph_name, vehicle_mgr, schedule_mgr,
                                                                      task)

            # wait_time = (min_sched_load_time - task_mgr.get_task(task_id).create_time).seconds
            # task_vehicle_wait_time_list.append([task_id, sched_vehicle, wait_time])

            # 앞으로 기다릴 시간은 작고, 지금까지 기다린 시간은 큰 vehicle을 선택하도록
            after_wait_time = (min_sched_load_time - n_time).seconds
            before_wait_time = (n_time - task_mgr.get_task(task_id).create_time).seconds
            task_vehicle_wait_time_list.append(
                [task_id, sched_vehicle, before_wait_time * 0.5 - after_wait_time, sched_vehicle.name, before_wait_time,
                 after_wait_time])

            unsched_vehicle_list[sched_vehicle.name] = True

            # sched_vehicles, sched_load_times = get_sched_time_vehicle(n_time, graph_name, vehicle_mgr, schedule_mgr, task)
            #
            # for sched_vehicle, sched_load_time in zip(sched_vehicles, sched_load_times):
            #     after_wait_time = (sched_load_time - n_time).seconds
            #     before_wait_time = (n_time - task_mgr.get_task(task_id).create_time).seconds
            #     task_vehicle_wait_time_list.append(
            #         [task_id, sched_vehicle, before_wait_time * 0.5 - after_wait_time, sched_vehicle.name, before_wait_time,
            #          after_wait_time])
            #
            #     unsched_vehicle_list[sched_vehicle.name] = True

        # 2. task별 Max Wait Time을 위한 정렬
        # task_vehicle_wait_time_list = sorted(task_vehicle_wait_time_list.items(), reverse=True)
        task_vehicle_wait_time_list.sort(key=lambda x: -x[2])
        # print(task_vehicle_wait_time_list)

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
