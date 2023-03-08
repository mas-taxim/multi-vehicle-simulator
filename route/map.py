import networkx as nx
import random

graph_dict = {}


def make_node_idx(node):
    node_idx = {}
    for key, value in node.items():
        node_idx[value] = key

    return node_idx


def get_yeouido_graph():
    if graph_dict.__contains__('yeouido'):
        return graph_dict['yeouido']

    graph = nx.Graph()

    node = {
        0: (37.52897, 126.917101),
        1: (37.529591, 126.918141),
        2: (37.529933, 126.918729),
        3: (37.530312, 126.919317),
        4: (37.5306824, 126.91990),
        5: (37.531043, 126.920470),
        6: (37.5314761, 126.92119),
        7: (37.5286005, 126.91910),
        8: (37.5289073, 126.919692),
        9: (37.529277, 126.920302),
        10: (37.5296559, 126.920879),
        11: (37.530016, 126.921467),
        12: (37.5268796, 126.919094),
        13: (37.527502, 126.920146),
        14: (37.527889, 126.920768),
        15: (37.528223, 126.921288),
        16: (37.528548, 126.921955),
        17: (37.528963, 126.922498),
        18: (37.529486, 126.923453),
    }

    graph.add_edge(0, 1, weight=1)
    graph.add_edge(1, 2, weight=1)
    graph.add_edge(2, 3, weight=1)
    graph.add_edge(3, 4, weight=1)
    graph.add_edge(4, 5, weight=1)
    graph.add_edge(5, 6, weight=1)
    graph.add_edge(7, 8, weight=1)
    graph.add_edge(8, 9, weight=1)
    graph.add_edge(9, 10, weight=1)
    graph.add_edge(10, 11, weight=1)
    graph.add_edge(12, 13, weight=1)
    graph.add_edge(13, 14, weight=1)
    graph.add_edge(14, 15, weight=1)
    graph.add_edge(15, 16, weight=1)
    graph.add_edge(16, 17, weight=1)
    graph.add_edge(17, 18, weight=1)

    graph.add_edge(1, 7, weight=1)
    graph.add_edge(2, 8, weight=1)
    graph.add_edge(3, 9, weight=1)
    graph.add_edge(4, 10, weight=1)
    graph.add_edge(5, 11, weight=1)

    graph.add_edge(7, 13, weight=1)
    graph.add_edge(8, 14, weight=1)
    graph.add_edge(9, 15, weight=1)
    graph.add_edge(10, 16, weight=1)
    graph.add_edge(11, 17, weight=1)

    graph.add_edge(6, 18, weight=1)

    node_idx = make_node_idx(node)
    graph_dict['yeouido'] = (node, node_idx, graph)
    return graph_dict['yeouido']


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

    graph.add_edge(0, 1, weight=2)
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
