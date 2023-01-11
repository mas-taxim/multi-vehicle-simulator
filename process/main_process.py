import datetime

from object.VehicleMgr import VehicleMgr
from object.TaskMgr import TaskMgr

from process.alloc_process import alloc_process
from process.vehicle_process import vehicle_process


def main_process(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):

    for i in range(10):
        v_name, t_idx = alloc_process(n_time, vehicle_mgr, task_mgr)
        if v_name is None:
            break

    vehicle_process(n_time, vehicle_mgr)

    print(n_time)
    print(vehicle_mgr.get_log())
    print(task_mgr.get_log())
