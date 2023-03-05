import networkx as nx
import random

graph_dict = {}


def make_node_idx(node):
    node_idx = {}
    for key, value in node.items():
        node_idx[value] = key

    return node_idx


def get_rectangle_graph():
    if graph_dict.__contains__('rectangle'):
        return graph_dict['rectangle']

    graph = nx.Graph()

    node = {
        0: (0, 0),
        1: (0, 2),
        2: (2, 2),
        3: (2, 0),
    }

    graph.add_edge(0, 1, weight=1)
    graph.add_edge(1, 2, weight=2)
    graph.add_edge(2, 3, weight=3)
    graph.add_edge(3, 0, weight=4)

    graph.add_edge(1, 0, weight=4)
    graph.add_edge(2, 1, weight=3)
    graph.add_edge(3, 2, weight=2)
    graph.add_edge(0, 3, weight=1)

    node_idx = make_node_idx(node)
    graph_dict['rectangle'] = (node, node_idx, graph)
    return graph_dict['rectangle']


def get_grid_graph():
    if graph_dict.__contains__('grid'):
        return graph_dict['grid']

    random.seed(0)
    graph = nx.Graph()

    node = {}

    idx = 0
    for i in [0, 5, 10, 15, 20]:
        for j in [0, 5, 10, 15, 20]:
            node[idx] = (i, j)
            idx += 1

    for i in range(5):
        for j in range(4):
            # print(5 * i + j, 5 * i + j + 1)
            graph.add_edge(5 * i + j, 5 * i + j + 1, weight=random.randint(1, 4))

    for i in range(5):
        for j in range(4):
            # print(5 * j + i, 5 * (j + 1) + i)
            graph.add_edge(5 * j + i, 5 * (j + 1) + i, weight=random.randint(1, 4))

    nx.draw(graph)

    node_idx = make_node_idx(node)
    graph_dict['grid'] = (node, node_idx, graph)
    return graph_dict['grid']
