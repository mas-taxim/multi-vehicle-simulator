from datetime import datetime

from entity import Location
from manager import TaskManager


def test_add_and_remove():
    task_manager = TaskManager()
    task_manager.add_task(0, Location(0, 10), Location(
        10, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)
    assert len(task_manager.tasks) == 1
    task_manager.remove_task(0)
    assert len(task_manager.tasks) == 0


def test_processing_task():
    task_manager = TaskManager()
    task_manager.add_task(0, Location(0, 10), Location(
        10, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)

    assert task_manager.get_task(0).idx == 0
    assert task_manager.get_task(0).loc_load.x == 0
    assert task_manager.get_task(0).loc_load.y == 10
    assert task_manager.get_task(
        0).create_time == datetime.strptime("2023-02-02", '%Y-%m-%d')
    assert task_manager.get_task(0).elapsed_time == 3
    assert task_manager.is_remain_wait_task() is True
    assert task_manager.peek_wait_task().idx == 0
    assert task_manager.peek_wait_task().idx == 0
    assert task_manager.poll_wait_task().idx == 0

    task_manager.add_task(1, Location(0, 10), Location(
        10, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)
    task_manager.add_task(2, Location(0, 10), Location(
        10, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)

    assert task_manager.poll_wait_task().idx == 1
    assert task_manager.poll_wait_task().idx == 2
    assert task_manager.poll_wait_task() is None

    assert len(task_manager.tasks) == 3
    assert len(task_manager.vehicles_alloced) == 3

    task_manager.remove_task(0)

    assert len(task_manager.tasks) == 2
    assert len(task_manager.vehicles_alloced) == 2
