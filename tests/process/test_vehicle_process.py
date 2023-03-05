import pytest
from datetime import datetime, timedelta

from object.Location import Location
from object.Vehicle import Vehicle
from object.VehicleMgr import VehicleMgr
from object.Task import Task
from object.TaskMgr import TaskMgr

from process.vehicle_process import vehicle_process, move
from allocator.vehicle_allocator import allocate

from route.route import get_graph


@pytest.fixture
def vehicle_mgr():
    vehicle_mgr: VehicleMgr = VehicleMgr()
    vehicle_mgr.add_vehicle("V1")
    vehicle_mgr.add_vehicle("V2")

    return vehicle_mgr


@pytest.fixture
def task_mgr():
    task_mgr: TaskMgr = TaskMgr()
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
    graph_name = 'rectangle'
    node, node_idx, graph = get_graph(graph_name)

    task_mgr.add_task(len(task_mgr.tasks), Location(node[0][0], node[0][1]),
                      Location(node[1][0], node[1][1]), n_time, 2)
    task_mgr.add_task(len(task_mgr.tasks), Location(node[2][0], node[2][1]),
                      Location(node[3][0], node[3][1]), n_time, 2)

    allocate(n_time, graph_name, vehicle_mgr, task_mgr, "V1", 0)
    vehicle = vehicle_mgr.get_vehicle("V1")

    print(vehicle.route)
    task = task_mgr.get_task(0)
    assert vehicle.status == Vehicle.ALLOC

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_LOAD

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.LOAD_START
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 0
    assert task.load_start_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.LOADING
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 0

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.LOADING
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 0

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.LOAD_END
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 0
    assert task.load_end_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 0

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 1

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 2

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.UNLOAD_START
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 2
    assert task.unload_start_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.UNLOADING
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 2

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.UNLOADING
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 2

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.UNLOAD_END
    assert vehicle.loc.x == 0
    assert vehicle.loc.y == 2
    assert task.unload_end_time == n_time

    n_time += timedelta(minutes=1)
    vehicle_process(n_time, vehicle_mgr)
    assert vehicle.status == Vehicle.WAIT
