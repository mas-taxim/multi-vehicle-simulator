from datetime import datetime, timedelta
import logging

from object.Location import Location
from object.VehicleMgr import VehicleMgr
from object.TaskMgr import TaskMgr

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

from process.main_process import main_process

def run():
    n_time: datetime = datetime.strptime("2023-02-02", '%Y-%m-%d')

    vehicle_mgr: VehicleMgr = VehicleMgr()
    vehicle_mgr.add_vehicle("V1")
    vehicle_mgr.add_vehicle("V2")

    task_mgr: TaskMgr = TaskMgr()

    task_mgr.add_task(0, Location(0, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 2)
    task_mgr.add_task(1, Location(3, 5), datetime.strptime("2023-02-02", '%Y-%m-%d'), 14)
    task_mgr.add_task(2, Location(2, 9), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)
    task_mgr.add_task(3, Location(8, 8), datetime.strptime("2023-02-02", '%Y-%m-%d'), 12)
    task_mgr.add_task(4, Location(9, 1), datetime.strptime("2023-02-02", '%Y-%m-%d'), 5)
    task_mgr.add_task(5, Location(1, 0), datetime.strptime("2023-02-02", '%Y-%m-%d'), 17)
    task_mgr.add_task(6, Location(2, 5), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)

    for i in range(50):
        n_time += timedelta(minutes=1)
        main_process(n_time, vehicle_mgr, task_mgr)


if __name__ == "__main__":
    run()