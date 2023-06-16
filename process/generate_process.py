import logging
import datetime
import random

from entity import Location
from manager import TaskManager

from graph.map import get_map

logger = logging.getLogger("main")
subgraph = None


def generate_task(n_time: datetime, node: dict, task_mgr: TaskManager, task: tuple):
    req_time, load_idx, unload_idx = task

    print(f"[generate_process] : generate task id : {len(task_mgr.tasks)}, time : {req_time[0:5]}")
    task_mgr.add_task(len(task_mgr.tasks),
                      Location(node[load_idx][0], node[load_idx][1]),
                      Location(node[unload_idx][0], node[unload_idx][1]),
                      n_time, random.randint(1, 3))


def generate_process(n_time: datetime, graph_name: str, task_mgr: TaskManager, tasks: list):
    node, node_idx, graph = get_map(graph_name)

    while len(tasks) > 0 and tasks[0][0][0:5] <= n_time.strftime('%H:%M'):
        generate_task(n_time, node, task_mgr, tasks[0])
        tasks.pop(0)
