import logging
import datetime
import random

from object.Location import Location
from object.TaskMgr import TaskMgr

logger = logging.getLogger("main")


def generate_process(n_time: datetime, task_mgr: TaskMgr, epsilon: float):
    if random.random() < epsilon:
        task_mgr.add_task(len(task_mgr.tasks), Location(random.randint(0, 20), random.randint(0, 20)),
                          Location(random.randint(0, 20), random.randint(0, 20)), n_time, random.randint(3, 10))
