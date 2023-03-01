import pytest
from datetime import datetime, timedelta

from object.Location import Location
from object.Vehicle import Vehicle
from object.VehicleMgr import VehicleMgr
from object.Task import Task
from object.TaskMgr import TaskMgr

from process.vehicle_process import vehicle_process, move
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
    task_mgr.add_task(0, Location(2, 2), Location(3, 3), datetime.strptime("2023-02-02", '%Y-%m-%d'), 2)
    task_mgr.add_task(1, Location(4, 1), Location(1, 4), datetime.strptime("2023-02-02", '%Y-%m-%d'), 1)

    return task_mgr


@pytest.fixture
def n_time():
    return datetime.strptime("2023-02-02", '%Y-%m-%d')


def test_move1(n_time: datetime, vehicle_mgr: VehicleMgr):
    vehicle: Vehicle = vehicle_mgr.get_vehicle("V1")
    point: Location = Location(0, 2)

    move(vehicle, point)
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 1

    move(vehicle, point)
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 2

    move(vehicle, point)
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 2


def test_script1(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    allocate(n_time, vehicle_mgr, task_mgr, "V1", 0)
    vehicle = vehicle_mgr.get_vehicle("V1")
    task = task_mgr.get_task(0)
    assert vehicle.status == Vehicle.ALLOC

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_LOAD

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_LOAD
    assert vehicle.loc.x == 1
    assert vehicle.loc.y == 0

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_LOAD
    assert vehicle.loc.x == 2
    assert vehicle.loc.y == 0

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_LOAD
    assert vehicle.loc.x == 2
    assert vehicle.loc.y == 1

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_LOAD
    assert vehicle.loc.x == 2
    assert vehicle.loc.y == 2

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.LOAD_START
    assert task.load_start_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.LOADING
    assert task.elapsed_time == 2

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.LOADING

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.LOAD_END
    assert task.load_end_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle.loc.x == 2
    assert vehicle.loc.y == 2

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle.loc.x == 3
    assert vehicle.loc.y == 2

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle.loc.x == 3
    assert vehicle.loc.y == 3

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.UNLOAD_START
    assert task.unload_start_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.UNLOADING

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.UNLOADING

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.UNLOAD_END
    assert task.unload_end_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.WAIT

