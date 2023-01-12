from datetime import datetime, timedelta
import logging
import random

from object.Location import Location
from object.VehicleMgr import VehicleMgr
from object.TaskMgr import TaskMgr

from process.main_process import main_process


def init_log():
    log_time = datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"

    sys_logger = logging.getLogger("main")
    sys_logger.setLevel(logging.WARNING)

    data_logger = logging.getLogger("data")
    data_logger.setLevel(logging.INFO)

    # log 출력
    sys_log_handler = logging.FileHandler(f'sys_log/{log_time}')
    sys_log_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    sys_logger.addHandler(sys_log_handler)

    data_log_handler = logging.FileHandler(f'log/{log_time}')
    data_log_handler.setFormatter(logging.Formatter('%(message)s'))
    data_logger.addHandler(data_log_handler)


def run():
    init_log()
    random.seed(0)

    n_time: datetime = datetime.strptime("2023-02-02", '%Y-%m-%d')

    vehicle_mgr: VehicleMgr = VehicleMgr()
    vehicle_mgr.add_vehicle("V1")
    vehicle_mgr.add_vehicle("V2")

    task_mgr: TaskMgr = TaskMgr()

    for i in range(10):
        task_mgr.add_task(i, Location(random.randint(0, 20), random.randint(0, 20)), n_time, random.randint(3, 10))

    for i in range(120):
        n_time += timedelta(minutes=1)
        main_process(n_time, vehicle_mgr, task_mgr)


if __name__ == "__main__":
    run()
