import pytest
from datetime import datetime

from object.Location import Location
from object.Vehicle import Vehicle
from object.Task import Task
from object.VehicleMgr import VehicleMgr
from object.TaskMgr import TaskMgr

from allocator.vehicle_allocator import allocate


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


def test_allocate(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    allocate(n_time, vehicle_mgr, task_mgr, "V1", 0)

    assert vehicle_mgr.tasks_alloced.get("V1").idx == 0
    assert task_mgr.vehicles_alloced.get(0).name == "V1"

    assert vehicle_mgr.get_vehicle("V1").get_route_tuple() == [(0, 10)]
