import pytest
from datetime import datetime, timedelta

from object.Location import Location
from object.VehicleMgr import VehicleMgr
from object.TaskMgr import TaskMgr

from process.alloc_process import alloc_process
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


def test_script1(n_time: datetime, vehicle_mgr: VehicleMgr, task_mgr: TaskMgr):
    graph_name = 'rectangle'
    node, node_idx, graph = get_graph(graph_name)

    task_mgr.add_task(len(task_mgr.tasks), Location(node[0][0], node[0][1]),
                      Location(node[1][0], node[1][1]), n_time, 3)
    task_mgr.add_task(len(task_mgr.tasks), Location(node[2][0], node[2][1]),
                      Location(node[3][0], node[3][1]), n_time, 3)

    assert len(task_mgr.wait_queue) == 2

    alloc_v, alloc_t = alloc_process(n_time, graph_name, vehicle_mgr, task_mgr)
    assert alloc_v == "V1"
    assert alloc_t == 0
    assert vehicle_mgr.tasks_alloced.get("V1").idx == 0
    assert task_mgr.vehicles_alloced.get(0).name == "V1"
    n_time += timedelta(minutes=1)
    assert vehicle_mgr.get_alloced_task("V1").alloc_time == datetime.strptime("2023-02-02", '%Y-%m-%d')
    assert len(task_mgr.wait_queue) == 1

    alloc_v, alloc_t = alloc_process(n_time, graph_name, vehicle_mgr, task_mgr)
    assert alloc_v == "V2"
    assert alloc_t == 1
    assert vehicle_mgr.tasks_alloced.get("V2").idx == 1
    assert task_mgr.vehicles_alloced.get(1).name == "V2"
    assert len(task_mgr.wait_queue) == 0

    alloc_v, alloc_t = alloc_process(n_time, graph_name, vehicle_mgr, task_mgr)
    assert alloc_v is None
    assert alloc_t is None

    task_mgr.add_task(len(task_mgr.tasks), Location(node[2][0], node[2][1]),
                      Location(node[3][0], node[3][1]), n_time, 3)

    alloc_v, alloc_t = alloc_process(n_time, graph_name, vehicle_mgr, task_mgr)
    assert alloc_v is None
    assert alloc_t is None
    assert len(task_mgr.wait_queue) == 1
