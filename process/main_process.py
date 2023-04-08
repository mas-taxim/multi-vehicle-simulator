import datetime

from manager import TaskManager, VehicleManager

from process.generate_process import generate_process
from process.alloc_process import alloc_process, alloc_process_nearest
from process.vehicle_process import vehicle_process

epsilon = 0.05


def set_epsilon(e: float):
    global epsilon
    epsilon = e


def main_process(
        n_time: datetime,
        graph_name: str,
        vehicle_mgr: VehicleManager,
        task_mgr: TaskManager) -> dict:
    ''' processing each time, return value is result log '''
    generate_process(n_time, graph_name, task_mgr, epsilon)

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
