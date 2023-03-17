import pytest
from datetime import datetime

from entity import Location
from manager import TaskManager, VehicleManager

from allocator.vehicle_allocator import allocate
from graph.route import get_graph


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
def n_time():
    return datetime.strptime("2023-02-02", '%Y-%m-%d')


def test_allocate(n_time: datetime, vehicle_mgr: VehicleManager, task_mgr: TaskManager):
    graph_name = 'rectangle'
    node, node_idx, graph = get_graph(graph_name)

    vehicle_mgr.get_vehicle("V1").loc.x = node[0][0]
    vehicle_mgr.get_vehicle("V1").loc.y = node[0][1]

    vehicle_mgr.get_vehicle("V2").loc.x = node[0][0]
    vehicle_mgr.get_vehicle("V2").loc.y = node[0][1]

    task_mgr.add_task(0, Location(node[0][0], node[0][1]), Location(
        node[1][0], node[1][1]), n_time, 3)
    task_mgr.add_task(1, Location(node[2][0], node[2][1]), Location(
        node[3][0], node[3][1]), n_time, 3)

    allocate(n_time, graph_name, vehicle_mgr, task_mgr, "V1", 0)

    assert vehicle_mgr.tasks_alloced.get("V1").idx == 0
    assert task_mgr.vehicles_alloced.get(0).name == "V1"
