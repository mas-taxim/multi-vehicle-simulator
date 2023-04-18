import pytest
from datetime import datetime, timedelta

from entity import Location, Vehicle
from manager import VehicleManager, TaskManager
from process.schedule_process import init_schedule, add_schedule, get_schedule, get_earliest_vehicle

from graph.route import get_map


@pytest.fixture
def vehicle_mgr():
    vehicle_mgr: VehicleManager = VehicleManager()
    vehicle_mgr.add_vehicle("V1")
    vehicle_mgr.add_vehicle("V2")

    init_schedule("V1")
    init_schedule("V2")

    return vehicle_mgr


@pytest.fixture
def task_mgr():
    task_mgr: TaskManager = TaskManager()
    return task_mgr


@pytest.fixture
def n_time():
    return datetime.strptime("2023-02-02", '%Y-%m-%d')


def test_script1(n_time: datetime, vehicle_mgr: VehicleManager, task_mgr: TaskManager):
    graph_name = 'rectangle'
    node, node_idx, graph = get_map(graph_name)

    vehicle_mgr.get_vehicle("V1").loc.x = node[0][0]
    vehicle_mgr.get_vehicle("V1").loc.y = node[0][1]
    vehicle_mgr.open_vehicle("V1", n_time + timedelta(hours=8))
    vehicle_mgr.get_vehicle("V1").status = Vehicle.WAIT

    vehicle_mgr.get_vehicle("V2").loc.x = node[0][0]
    vehicle_mgr.get_vehicle("V2").loc.y = node[0][1]
    vehicle_mgr.open_vehicle("V2", n_time + timedelta(minutes=1))
    vehicle_mgr.get_vehicle("V2").status = Vehicle.WAIT

    task_mgr.add_task(len(task_mgr.tasks), Location(
        node[1][0], node[1][1]), Location(node[0][0], node[0][1]), n_time, 1)
    task_mgr.add_task(len(task_mgr.tasks), Location(
        node[2][0], node[2][1]), Location(node[3][0], node[3][1]), n_time, 1)

    sched_vehicle = get_earliest_vehicle(n_time, graph_name, vehicle_mgr, task_mgr.get_task(0))
    assert sched_vehicle.name == "V1"

    add_schedule(n_time, graph_name, sched_vehicle, task_mgr.get_task(0))
    schedule_v1 = get_schedule(sched_vehicle.name)

    assert schedule_v1[0].task_id == -1
    assert schedule_v1[0].start_time == datetime.strptime("2023-02-02", '%Y-%m-%d')
    assert schedule_v1[0].start_loc.x == 0
    assert schedule_v1[0].start_loc.y == 0
    assert schedule_v1[0].end_time == datetime.strptime("2023-02-02 00:01:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_v1[0].end_loc.x == 0
    assert schedule_v1[0].end_loc.y == 2

    assert schedule_v1[1].task_id == 0
    assert schedule_v1[1].start_time == datetime.strptime("2023-02-02 00:01:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_v1[1].start_loc.x == 0
    assert schedule_v1[1].start_loc.y == 2
    assert schedule_v1[1].end_time == datetime.strptime("2023-02-02 00:04:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_v1[1].end_loc.x == 0
    assert schedule_v1[1].end_loc.y == 0

    sched_vehicle = get_earliest_vehicle(n_time, graph_name, vehicle_mgr, task_mgr.get_task(1))
    assert sched_vehicle.name == "V1"

    add_schedule(n_time, graph_name, sched_vehicle, task_mgr.get_task(1))
    schedule_v1 = get_schedule(sched_vehicle.name)

    assert schedule_v1[2].task_id == -1
    assert schedule_v1[2].start_time == datetime.strptime("2023-02-02 00:04:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_v1[2].start_loc.x == 0
    assert schedule_v1[2].start_loc.y == 0
    assert schedule_v1[2].end_time == datetime.strptime("2023-02-02 00:06:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_v1[2].end_loc.x == 2
    assert schedule_v1[2].end_loc.y == 2

    assert schedule_v1[3].task_id == 1
    assert schedule_v1[3].start_time == datetime.strptime("2023-02-02 00:06:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_v1[3].start_loc.x == 2
    assert schedule_v1[3].start_loc.y == 2
    assert schedule_v1[3].end_time == datetime.strptime("2023-02-02 00:07:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_v1[3].end_loc.x == 2
    assert schedule_v1[3].end_loc.y == 0
