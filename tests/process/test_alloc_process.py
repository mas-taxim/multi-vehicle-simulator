import pytest
from datetime import datetime, timedelta

from object.Location import Location
from object.Vehicle import Vehicle
from object.VehicleMgr import VehicleMgr
from object.Task import Task
from object.TaskMgr import TaskMgr

from process.alloc_process import alloc_process


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


def test_script1(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    assert len(task_mgr.wait_queue) == 2

    alloc_v, alloc_t = alloc_process(n_time, vehicle_mgr, task_mgr)
    assert alloc_v == "V1"
    assert alloc_t == 0
    assert vehicle_mgr.tasks_alloced.get("V1").idx == 0
    assert task_mgr.vehicles_alloced.get(0).name == "V1"
    n_time += timedelta(hours=1)
    assert vehicle_mgr.get_alloced_task("V1").alloc_time == datetime.strptime("2023-02-02", '%Y-%m-%d')
    assert len(task_mgr.wait_queue) == 1

    alloc_v, alloc_t = alloc_process(n_time, vehicle_mgr, task_mgr)
    assert alloc_v == "V2"
    assert alloc_t == 1
    assert vehicle_mgr.tasks_alloced.get("V2").idx == 1
    assert task_mgr.vehicles_alloced.get(1).name == "V2"
    assert len(task_mgr.wait_queue) == 0

    alloc_v, alloc_t = alloc_process(n_time, vehicle_mgr, task_mgr)
    assert alloc_v is None
    assert alloc_t is None

    task_mgr.add_task(2, Location(10, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)

    alloc_v, alloc_t = alloc_process(n_time, vehicle_mgr, task_mgr)
    assert alloc_v is None
    assert alloc_t is None
    assert len(task_mgr.wait_queue) == 1
