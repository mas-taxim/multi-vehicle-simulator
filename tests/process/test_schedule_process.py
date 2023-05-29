import pytest
from datetime import datetime, timedelta

from entity import Location, Vehicle
from manager import VehicleManager, TaskManager, ScheduleManager
from process.schedule_process import add_schedule, get_earliest_vehicle

from graph.route import get_map


@pytest.fixture
def vehicle_mgr():
    vehicle_mgr: VehicleManager = VehicleManager()
    vehicle_mgr.add_vehicle("V1")
    vehicle_mgr.add_vehicle("V2")

    return vehicle_mgr


@pytest.fixture
def task_mgr():
    task_mgr: TaskManager = TaskManager()
    return task_mgr


@pytest.fixture
def schedule_mgr():
    schedule_mgr: ScheduleManager = ScheduleManager()
    return schedule_mgr


@pytest.fixture
def n_time():
    return datetime.strptime("2023-02-02", '%Y-%m-%d')


def test_script1(n_time: datetime, vehicle_mgr: VehicleManager, task_mgr: TaskManager, schedule_mgr: ScheduleManager):
    graph_name = 'rectangle'
    node, node_idx, graph = get_map(graph_name)

    schedule_mgr.init_schedule("V1")
    schedule_mgr.init_schedule("V2")

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

    sched_vehicle, min_sched_load_time = get_earliest_vehicle(n_time, graph_name, vehicle_mgr, schedule_mgr, task_mgr.get_task(0))
    assert sched_vehicle.name == "V1"

    add_schedule(n_time, graph_name, sched_vehicle, task_mgr.get_task(0), schedule_mgr)

    schedule_list_v1 = schedule_mgr.get_schedule_list(sched_vehicle.name)

    assert schedule_list_v1.get_schedule(0).task_id == 0
    assert schedule_list_v1.get_schedule(0).start_time == datetime.strptime("2023-02-02", '%Y-%m-%d')
    assert schedule_list_v1.get_schedule(0).start_loc.x == 0
    assert schedule_list_v1.get_schedule(0).start_loc.y == 0
    # moving : 1, elapsed : 1, processing: 3
    assert schedule_list_v1.get_schedule(0).load_time == datetime.strptime("2023-02-02 00:05:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_list_v1.get_schedule(0).load_loc.x == 0
    assert schedule_list_v1.get_schedule(0).load_loc.y == 2
    # moving : 3, elapsed : 1, processing: 3
    assert schedule_list_v1.get_schedule(0).unload_time == datetime.strptime("2023-02-02 00:12:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_list_v1.get_schedule(0).unload_loc.x == 0
    assert schedule_list_v1.get_schedule(0).unload_loc.y == 0

    sched_vehicle, min_sched_load_time = get_earliest_vehicle(n_time, graph_name, vehicle_mgr, schedule_mgr, task_mgr.get_task(1))
    assert sched_vehicle.name == "V1"

    add_schedule(n_time, graph_name, sched_vehicle, task_mgr.get_task(1), schedule_mgr)

    schedule_list_v1 = schedule_mgr.get_schedule_list(sched_vehicle.name)

    assert schedule_list_v1.get_schedule(1).task_id == 1
    assert schedule_list_v1.get_schedule(1).start_time == datetime.strptime("2023-02-02 00:12:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_list_v1.get_schedule(1).start_loc.x == 0
    assert schedule_list_v1.get_schedule(1).start_loc.y == 0
    assert schedule_list_v1.get_schedule(1).load_time == datetime.strptime("2023-02-02 00:18:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_list_v1.get_schedule(1).load_loc.x == 2
    assert schedule_list_v1.get_schedule(1).load_loc.y == 2
    assert schedule_list_v1.get_schedule(1).unload_time == datetime.strptime("2023-02-02 00:23:00", '%Y-%m-%d %H:%M:%S')
    assert schedule_list_v1.get_schedule(1).unload_loc.x == 2
    assert schedule_list_v1.get_schedule(1).unload_loc.y == 0
