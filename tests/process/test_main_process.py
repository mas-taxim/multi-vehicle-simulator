import pytest
from datetime import datetime, timedelta

from object.Location import Location
from object.Vehicle import Vehicle
from object.VehicleMgr import VehicleMgr
from object.Task import Task
from object.TaskMgr import TaskMgr

from process.main_process import main_process


@pytest.fixture
def vehicle_mgr():
    vehicle_mgr: VehicleMgr = VehicleMgr()
    vehicle_mgr.add_vehicle("V1")
    vehicle_mgr.add_vehicle("V2")

    return vehicle_mgr


@pytest.fixture
def task_mgr():
    task_mgr: TaskMgr = TaskMgr()
    task_mgr.add_task(0, Location(0, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)
    task_mgr.add_task(1, Location(10, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)

    return task_mgr


@pytest.fixture
def n_time():
    return datetime.strptime("2023-02-02", '%Y-%m-%d')


def test_main_process1(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    main_process(n_time, vehicle_mgr, task_mgr)

    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVING
    assert vehicle_mgr.get_alloced_task("V1").idx == 0
    assert vehicle_mgr.get_vehicle("V1").loc.x == 0
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1
