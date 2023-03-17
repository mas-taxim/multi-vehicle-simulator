import pytest
from datetime import datetime, timedelta

from object.Location import Location
from object.Vehicle import Vehicle
from object.VehicleManager import VehicleManager
from object.Task import Task
from object.TaskManager import TaskManager

from process.main_process import main_process, set_epsilon

from route.route import get_graph


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


def test_main_process(n_time: datetime, vehicle_manager: VehicleManager, task_manager: TaskManager):
    set_epsilon(0)
    graph_name = 'rectangle'
    node, node_idx, graph = get_graph(graph_name)

    vehicle_manager.get_vehicle("V1").loc.x = node[0][0]
    vehicle_manager.get_vehicle("V1").loc.y = node[0][1]

    vehicle_manager.get_vehicle("V2").loc.x = node[0][0]
    vehicle_manager.get_vehicle("V2").loc.y = node[0][1]

    task_manager.add_task(len(task_manager.tasks), Location(node[0][0], node[0][1]),
                          Location(node[1][0], node[1][1]), n_time, 1)
    task_manager.add_task(len(task_manager.tasks), Location(node[2][0], node[2][1]),
                          Location(node[3][0], node[3][1]), n_time, 1)

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_manager.get_alloced_task("V1").idx == 0
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 0

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_manager.get_alloced_task("V2").idx == 1
    assert vehicle_manager.get_vehicle("V2").loc.x == 0
    assert vehicle_manager.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.LOAD_START
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 0

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_manager.get_vehicle("V2").loc.x == 0
    assert vehicle_manager.get_vehicle("V2").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.LOADING
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 0

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.MOVE_TO_LOAD
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.LOAD_END
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 0

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.LOAD_START
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 0

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.LOADING
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 2

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.LOAD_END
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.UNLOAD_START
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 2

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 2

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.UNLOADING
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 2

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.MOVE_TO_UNLOAD
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.UNLOAD_END
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 2

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.UNLOAD_START
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V1").status == Vehicle.WAIT
    assert vehicle_manager.get_vehicle("V1").loc.x == 0
    assert vehicle_manager.get_vehicle("V1").loc.y == 2

    assert vehicle_manager.get_vehicle("V2").status == Vehicle.UNLOADING
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V2").status == Vehicle.UNLOAD_END
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 0

    n_time += timedelta(minutes=1)
    main_process(n_time, graph_name, vehicle_manager, task_manager)
    assert vehicle_manager.get_vehicle("V2").status == Vehicle.WAIT
    assert vehicle_manager.get_vehicle("V2").loc.x == 2
    assert vehicle_manager.get_vehicle("V2").loc.y == 0
