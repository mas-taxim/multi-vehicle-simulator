import pytest

from datetime import datetime, timedelta

from entity import Location, Vehicle
from manager import TaskManager, VehicleManager
from process.alloc_process import alloc_process
from graph.route import get_map


@pytest.fixture
def vehicle_manager():
    manager: VehicleManager = VehicleManager()
    manager.add_vehicle("V1")
    manager.add_vehicle("V2")

    return manager


@pytest.fixture
def task_manager():
    manager: TaskManager = TaskManager()
    return manager


@pytest.fixture
def n_time():
    return datetime.strptime("2023-02-02", '%Y-%m-%d')


def test_script1(
        n_time: datetime,
        vehicle_manager: VehicleManager,
        task_manager: TaskManager):
    graph_name = 'rectangle'
    node, node_idx, graph = get_map(graph_name)

    vehicle_manager.get_vehicle("V1").loc.x = node[0][0]
    vehicle_manager.get_vehicle("V1").loc.y = node[0][1]
    vehicle_manager.open_vehicle("V1")
    vehicle_manager.get_vehicle("V1").status = Vehicle.WAIT

    vehicle_manager.get_vehicle("V2").loc.x = node[0][0]
    vehicle_manager.get_vehicle("V2").loc.y = node[0][1]
    vehicle_manager.open_vehicle("V2")
    vehicle_manager.get_vehicle("V2").status = Vehicle.WAIT

    task_manager.add_task(len(task_manager.tasks), Location(
        node[0][0], node[0][1]), Location(node[1][0], node[1][1]), n_time, 3)
    task_manager.add_task(len(task_manager.tasks), Location(
        node[2][0], node[2][1]), Location(node[3][0], node[3][1]), n_time, 3)

    assert len(task_manager.wait_queue) == 2

    alloc_v, alloc_t = alloc_process(n_time, graph_name, vehicle_manager, task_manager)
    assert alloc_v == "V1"
    assert alloc_t == 0
    assert vehicle_manager.tasks_alloced.get("V1").idx == 0
    assert task_manager.vehicles_alloced.get(0).name == "V1"
    n_time += timedelta(minutes=1)
    assert vehicle_manager.get_alloced_task(
        "V1").alloc_time == datetime.strptime("2023-02-02", '%Y-%m-%d')
    assert len(task_manager.wait_queue) == 1

    alloc_v, alloc_t = alloc_process(n_time, graph_name, vehicle_manager, task_manager)
    assert alloc_v == "V2"
    assert alloc_t == 1
    assert vehicle_manager.tasks_alloced.get("V2").idx == 1
    assert task_manager.vehicles_alloced.get(1).name == "V2"
    assert len(task_manager.wait_queue) == 0

    alloc_v, alloc_t = alloc_process(n_time, graph_name, vehicle_manager, task_manager)
    assert alloc_v is None
    assert alloc_t is None

    task_manager.add_task(len(task_manager.tasks), Location(
        node[2][0], node[2][1]), Location(node[3][0], node[3][1]), n_time, 3)

    alloc_v, alloc_t = alloc_process(n_time, graph_name, vehicle_manager, task_manager)
    assert alloc_v is None
    assert alloc_t is None
    assert len(task_manager.wait_queue) == 1
