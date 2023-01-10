import pytest
from datetime import datetime, timedelta

from object.Location import Location
from object.Vehicle import Vehicle
from object.VehicleMgr import VehicleMgr
from object.Task import Task
from object.TaskMgr import TaskMgr

from process.vehicle_process import vehicle_process, move, execute_task, re_prepare
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
    task_mgr.add_task(0, Location(2, 2), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)
    task_mgr.add_task(1, Location(4, 1), datetime.strptime("2023-02-02", '%Y-%m-%d'), 1)

    return task_mgr


@pytest.fixture
def n_time():
    return datetime.strptime("2023-02-02", '%Y-%m-%d')


def test_move1(n_time: datetime, vehicle_mgr: VehicleMgr):
    vehicle: Vehicle = vehicle_mgr.get_vehicle("V1")
    point: Location = Location(0, 2)

    move(n_time, vehicle_mgr, vehicle, point)
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 1

    move(n_time, vehicle_mgr, vehicle, point)
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 2

    move(n_time, vehicle_mgr, vehicle, point)
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 2


def test_script1(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    allocate(n_time, vehicle_mgr, task_mgr, "V1", 0)

    n_time += timedelta(minutes=1)
    move(n_time, vehicle_mgr, vehicle_mgr.get_vehicle("V1"))
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 0
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVING

    n_time += timedelta(minutes=1)
    move(n_time, vehicle_mgr, vehicle_mgr.get_vehicle("V1"))
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 0
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVING

    n_time += timedelta(minutes=1)
    move(n_time, vehicle_mgr, vehicle_mgr.get_vehicle("V1"))
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVING

    n_time += timedelta(minutes=1)
    move(n_time, vehicle_mgr, vehicle_mgr.get_vehicle("V1"))
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.ARRIVE

    n_time += timedelta(minutes=1)
    execute_task(n_time, vehicle_mgr, vehicle_mgr.get_vehicle("V1"))
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.WORKING

    n_time += timedelta(minutes=1)
    execute_task(n_time, vehicle_mgr, vehicle_mgr.get_vehicle("V1"))
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.WORKING

    n_time += timedelta(minutes=1)
    execute_task(n_time, vehicle_mgr, vehicle_mgr.get_vehicle("V1"))
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.WORKING

    n_time += timedelta(minutes=1)
    execute_task(n_time, vehicle_mgr, vehicle_mgr.get_vehicle("V1"))
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.DONE


def test_script2(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    allocate(n_time, vehicle_mgr, task_mgr, "V1", 0)
    allocate(n_time, vehicle_mgr, task_mgr, "V2", 1)

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 0
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVING
    assert task_mgr.get_task(0).move_time == n_time

    assert vehicle_mgr.get_vehicle("V2").loc.x == 1
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0
    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVING
    assert task_mgr.get_task(1).move_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 0
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVING

    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0
    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVING

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVING

    assert vehicle_mgr.get_vehicle("V2").loc.x == 3
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0
    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVING

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.ARRIVE
    assert task_mgr.get_task(0).arrive_time == n_time

    assert vehicle_mgr.get_vehicle("V2").loc.x == 4
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0
    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVING

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.WORKING
    assert task_mgr.get_task(0).work_time == n_time

    assert vehicle_mgr.get_vehicle("V2").loc.x == 4
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1
    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.ARRIVE
    assert task_mgr.get_task(1).arrive_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.WORKING

    assert vehicle_mgr.get_vehicle("V2").loc.x == 4
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1
    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.WORKING
    assert task_mgr.get_task(1).work_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.WORKING
    assert task_mgr.get_task(0).done_time is None

    assert vehicle_mgr.get_vehicle("V2").loc.x == 4
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1
    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.DONE
    assert task_mgr.get_task(1).done_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.DONE
    assert task_mgr.get_task(0).done_time == n_time

    assert vehicle_mgr.get_vehicle("V2").loc.x == 4
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1
    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.WAIT
