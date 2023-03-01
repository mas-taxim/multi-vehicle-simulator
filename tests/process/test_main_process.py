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
    task_mgr.add_task(0, Location(0, 1), Location(1, 1), datetime.strptime("2023-02-02", '%Y-%m-%d'), 2)
    task_mgr.add_task(1, Location(1, 1), Location(2, 0), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)
    task_mgr.add_task(2, Location(3, 2), Location(1, 2), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)

    return task_mgr


@pytest.fixture
def n_time():
    return datetime.strptime("2023-02-02", '%Y-%m-%d')


def test_main_process1(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_mgr.get_alloced_task("V1").idx == 0
    assert vehicle_mgr.get_vehicle("V1").loc.x == 0
    assert vehicle_mgr.get_vehicle("V1").loc.y == 0

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_mgr.get_alloced_task("V2").idx == 1
    assert vehicle_mgr.get_vehicle("V2").loc.x == 0
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_mgr.get_vehicle("V1").loc.x == 0
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_mgr.get_vehicle("V2").loc.x == 1
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.LOAD_START
    assert vehicle_mgr.get_vehicle("V1").loc.x == 0
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_mgr.get_vehicle("V2").loc.x == 1
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.LOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 0
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.LOAD_START
    assert vehicle_mgr.get_vehicle("V2").loc.x == 1
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.LOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 0
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.LOADING
    assert vehicle_mgr.get_vehicle("V2").loc.x == 1
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.LOAD_END
    assert vehicle_mgr.get_vehicle("V1").loc.x == 0
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.LOADING
    assert vehicle_mgr.get_vehicle("V2").loc.x == 1
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_mgr.get_vehicle("V1").loc.x == 0
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.LOADING
    assert vehicle_mgr.get_vehicle("V2").loc.x == 1
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.LOAD_END
    assert vehicle_mgr.get_vehicle("V2").loc.x == 1
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.UNLOAD_START
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_mgr.get_vehicle("V2").loc.x == 1
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.UNLOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 1

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.UNLOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.UNLOAD_END
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.UNLOAD_START
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.WAIT
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.UNLOADING
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_mgr.get_alloced_task("V1").idx == 2
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.UNLOADING
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.UNLOADING
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_mgr.get_vehicle("V1").loc.x == 3
    assert vehicle_mgr.get_vehicle("V1").loc.y == 1

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.UNLOAD_END
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_mgr.get_vehicle("V1").loc.x == 3
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.WAIT
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.LOAD_START
    assert vehicle_mgr.get_vehicle("V1").loc.x == 3
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.WAIT
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.LOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 3
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.LOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 3
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.LOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 3
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.LOAD_END
    assert vehicle_mgr.get_vehicle("V1").loc.x == 3
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_mgr.get_vehicle("V1").loc.x == 3
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_mgr.get_vehicle("V1").loc.x == 2
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.UNLOAD_START
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.UNLOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.UNLOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.UNLOADING
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.UNLOAD_END
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, vehicle_mgr, task_mgr)
    assert vehicle_mgr.get_vehicle("V1").status == Vehicle.WAIT
    assert vehicle_mgr.get_vehicle("V1").loc.x == 1
    assert vehicle_mgr.get_vehicle("V1").loc.y == 2

    assert vehicle_mgr.get_vehicle("V2").status == Vehicle.WAIT
    assert vehicle_mgr.get_vehicle("V2").loc.x == 2
    assert vehicle_mgr.get_vehicle("V2").loc.y == 0
