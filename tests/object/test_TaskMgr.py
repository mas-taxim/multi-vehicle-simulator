import pytest
from datetime import datetime

from object.Location import Location
from object.TaskMgr import TaskMgr


def test_script1():
    task_mgr = TaskMgr()
    task_mgr.add_task(0, Location(0, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)

    assert task_mgr.get_task(0).idx == 0
    assert task_mgr.get_task(0).loc.x == 0
    assert task_mgr.get_task(0).loc.y == 10
    assert task_mgr.get_task(0).create_time == datetime.strptime("2023-02-02", '%Y-%m-%d')
    assert task_mgr.get_task(0).elapsed_time == 3
    assert task_mgr.get_first_wait_task().idx == 0

    task_mgr.add_task(1, Location(0, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)
    task_mgr.add_task(2, Location(0, 10), datetime.strptime("2023-02-02", '%Y-%m-%d'), 3)

    assert task_mgr.get_first_wait_task().idx == 1
    assert task_mgr.get_first_wait_task().idx == 2
    assert task_mgr.get_first_wait_task() is None

    assert len(task_mgr.tasks) == 3
    assert len(task_mgr.vehicles_alloced) == 3

    task_mgr.remove_task(0)

    assert len(task_mgr.tasks) == 2
    assert len(task_mgr.vehicles_alloced) == 2



