import logging
import datetime
import random

from entity import Location
from manager import TaskManager

from graph.route import get_map

logger = logging.getLogger("main")
subgraph = None

def generate_task(n_time: datetime, node: dict, task_mgr: TaskManager, sub_graph):
    # load_idx, unload_idx = random.sample(node.keys(), 2)

    node, node_idx, graph = get_map('seoul_all')

    # 임시
    import networkx as nx
    try:
        load_idx, unload_idx = random.sample(sub_graph, 2)
        distance = nx.shortest_path_length(graph, load_idx, unload_idx, weight='weight')

        task_mgr.add_task(len(task_mgr.tasks),
                          Location(node[load_idx][0], node[load_idx][1]),
                          Location(node[unload_idx][0], node[unload_idx][1]),
                          n_time, random.randint(2, 5))
    except:
        None


def generate_process(n_time: datetime, graph_name: str, task_mgr: TaskManager, epsilon: float):
    node, node_idx, graph = get_map(graph_name)

    # 임시
    if subgraph is None:
        import networkx as nx
        sub_graph = list(nx.connected_components(graph.to_undirected()))[0]

    if random.random() < epsilon:
        generate_task(n_time, node, task_mgr, sub_graph)
