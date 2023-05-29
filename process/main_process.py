import datetime

from manager import TaskManager, VehicleManager, ScheduleManager

from process.generate_process import generate_process
from process.schedule_process import schedule_process, reschedule_process, swap_process
from process.alloc_process import alloc_process, alloc_process_nearest, alloc_by_schedule
from process.vehicle_process import vehicle_process

epsilon = 0.05


def set_epsilon(e: float):
    global epsilon
    epsilon = e


def main_process(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        task_mgr: TaskManager,
        tasks) -> dict:
    ''' processing each time, return value is result log '''
    generate_process(n_time, graph_name, task_mgr, tasks)

    for i in range(len(vehicle_mgr.vehicles)):
        v_name, t_idx = alloc_process_nearest(
            n_time, graph_name, vehicle_mgr, task_mgr)
        if v_name is None:
            break

    vehicle_process(n_time, vehicle_mgr)

    log = dict()

    log['time'] = int(n_time.timestamp() * 1000)
    log['vehicles'] = vehicle_mgr.get_log()
    log['tasks'] = task_mgr.get_log()

    return log


def main_process_schedule(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        task_mgr: TaskManager,
        schedule_mgr: ScheduleManager,
        tasks,
        schedule_type: str,
        reschedule_time: int) -> dict:
    '''
    processing each time, return value is result log, schedule log
    schedule_type :
        dispatch - basic
        reschedule - every 5 min, reschedule all task and vehicle
    '''
    generate_process(n_time, graph_name, task_mgr, tasks)

    while task_mgr.get_wait_task_num() > 0:
        v_name, t_idx = schedule_process(n_time, graph_name, vehicle_mgr, task_mgr, schedule_mgr)
        if v_name is None:
            break

    if schedule_type == "reschedule" and (n_time.minute % reschedule_time) == 0:
        print(f"[schedule_process] : reschedule time : {n_time.strftime('%Y-%m-%d %H:%M:%S')}")
        reschedule_process(n_time, graph_name, vehicle_mgr, task_mgr, schedule_mgr)

    if schedule_type == "swap" and (n_time.minute % reschedule_time) == 0:
        print(f"[schedule_process] : swap time : {n_time.strftime('%Y-%m-%d %H:%M:%S')}")
        swap_process(n_time, graph_name, vehicle_mgr, task_mgr, schedule_mgr)

    alloc_by_schedule(n_time, graph_name, vehicle_mgr, task_mgr, schedule_mgr)

    vehicle_process(n_time, vehicle_mgr, schedule_mgr)

    log = dict()

    log['time'] = int(n_time.timestamp() * 1000)
    log['vehicles'] = vehicle_mgr.get_log()
    log['tasks'] = task_mgr.get_log()

    schedule_log = dict()
    if n_time.minute % 30 == 0:
        schedule_log['time'] = int(n_time.timestamp() * 1000)
        schedule_log['logs'] = schedule_mgr.get_logs()

    return log, schedule_log
