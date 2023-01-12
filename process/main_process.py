import datetime
import logging
import json

from object.VehicleMgr import VehicleMgr
from object.TaskMgr import TaskMgr

from process.alloc_process import alloc_process
from process.vehicle_process import vehicle_process

data_logger = logging.getLogger("data")


def main_process(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    for i in range(10):
        v_name, t_idx = alloc_process(n_time, vehicle_mgr, task_mgr)
        if v_name is None:
            break

    vehicle_process(n_time, vehicle_mgr)

    log = dict()

    log['n_time'] = n_time.strftime("%Y-%m-%d %H:%M:%S")
    log['vehicle'] = vehicle_mgr.get_log()
    log['task'] = task_mgr.get_log()

    data_logger.info(json.dumps(log))


