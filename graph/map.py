import networkx as nx
import json
import random
import os

cwd = os.path.abspath(os.path.dirname(__file__))

now_hour = 1
graph_dict = {}
random.seed(0)


def make_node_idx(node):
    node_idx = {}
    for key, value in node.items():
        node_idx[value] = key

    return node_idx


def make_graph(graph_name, hour):
    path = os.path.join(cwd, f"data/{graph_name}.json")
    with open(path, "r") as graph_file:
        graph_json = json.load(graph_file)

    graph = nx.DiGraph()
    nodes = {}

    print(f"make graph node, hour:{hour}")
    for node in graph_json['nodes']:
        nodes[node['id']] = (node['lat'], node['lng'])

    print(f"make graph edge, hour:{hour}")
    for edge in graph_json['edges']:
        graph.add_edge(edge['from'], edge['to'], weight=edge['info']['weight'][str(hour)])

    node_idx = make_node_idx(nodes)
    return nodes, node_idx, graph


def update_weight(graph_name, hour):
    nodes, node_idx, graph = make_graph(graph_name, hour)
    graph_dict[graph_name] = (nodes, node_idx, graph)

    global now_hour
    now_hour = hour


def get_hour():
    global now_hour
    return now_hour


def get_map(graph_name) -> (dict, dict, nx.DiGraph):
    if graph_dict.__contains__(graph_name):
        return graph_dict[graph_name]

    nodes, node_idx, graph = make_graph(graph_name, 1)
    graph_dict[graph_name] = (nodes, node_idx, graph)

    global now_hour
    now_hour = 1
    return graph_dict[graph_name]
