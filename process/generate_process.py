import logging
import datetime
import random

from object.Location import Location
from object.TaskMgr import TaskMgr

from route.route import get_graph

logger = logging.getLogger("main")


def generate_task(n_time: datetime, node: dict, task_mgr: TaskMgr):
    load_idx, unload_idx = random.sample(node.keys(), 2)
    task_mgr.add_task(len(task_mgr.tasks), Location(node[load_idx][0], node[load_idx][1]),
                      Location(node[unload_idx][0], node[unload_idx][1]), n_time, random.randint(3, 10))


def generate_process(n_time: datetime, graph_name: str, task_mgr: TaskMgr, epsilon: float):
    node, node_idx, graph = get_graph(graph_name)

    if random.random() < epsilon:
        generate_task(n_time, node, task_mgr)
