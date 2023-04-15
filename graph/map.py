import networkx as nx
import json
import random

graph_dict = {}
random.seed(0)


def make_node_idx(node):
    node_idx = {}
    for key, value in node.items():
        node_idx[value] = key

    return node_idx


def make_graph(graph_name, hour):
    with open(f"graph/data/{graph_name}.json", "r") as graph_file:
        graph_json = json.load(graph_file)

    graph = nx.DiGraph()
    nodes = {}

    for node in graph_json['nodes']:
        nodes[node['id']] = (node['lat'], node['lng'])

    for edge in graph_json['edges']:
        graph.add_edge(edge['from'], edge['to'], weight=edge['info']['weight'][str(hour)])

    node_idx = make_node_idx(nodes)
    return nodes, node_idx, graph
