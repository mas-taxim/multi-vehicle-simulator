import networkx as nx
import random
import math

graph_dict = {}
random.seed(0)


def make_node_idx(node):
    node_idx = {}
    for key, value in node.items():
        node_idx[value] = key

    return node_idx


def get_seoul_gu_graph():
    if graph_dict.__contains__('seoul_gu'):
        return graph_dict['seoul_gu']

    graph = nx.DiGraph()

    node = {
        0: (37.5173319, 127.0473774),  # 강남구청
        1: (37.5301933, 127.1237925),  # 강동구청
        2: (37.6397513, 127.0255380),  # 강북구청
        3: (37.5509646, 126.8495337),  # 강서구청
        4: (37.4783683, 126.9515618),  # 관악구청
        5: (37.5385583, 127.0823851),  # 광진구청
        6: (37.4954330, 126.8875053),  # 구로구청
        7: (37.4568411, 126.8954567),  # 금천구청
        8: (37.6543617, 127.0564304),  # 노원구청
        9: (37.6686914, 127.0472104),  # 도봉구청
        10: (37.5744184, 127.0397473),  # 동대문구청
        11: (37.5124820, 126.9393150),  # 동작구청
        12: (37.5662141, 126.9019551),  # 마포구청
        13: (37.5791618, 126.9368156),  # 서대문구청
        14: (37.4835870, 127.0327322),  # 서초구청
        15: (37.5634272, 127.0369301),  # 성동구청
        16: (37.5893588, 127.0167006),  # 성북구청
        17: (37.5145837, 127.1059177),  # 송파구청
        18: (37.5169884, 126.8665014),  # 양천구청
        19: (37.5263617, 126.8962716),  # 영등포구청
        20: (37.5324256, 126.9905755),  # 용산구청
        21: (37.6028174, 126.9289387),  # 은평구청
        22: (37.5735042, 126.9789899),  # 종로구청
        23: (37.5638077, 126.9975551),  # 서울특별시중구청
        24: (37.6065432, 127.0928202),  # 중랑구청
    }

    for i in node.keys():
        for j in node.keys():
            distance = math.sqrt(
                (node[i][0] - node[j][0]) ** 2 + (node[i][1] - node[j][1]) ** 2)
            if i != j and distance < 0.1:
                w = random.randint(2, 4)
                graph.add_edge(i, j, weight=w)
                graph.add_edge(j, i, weight=w)

    node_idx = make_node_idx(node)
    graph_dict['seoul_gu'] = (node, node_idx, graph)
    return graph_dict['seoul_gu']


def get_yeouido_graph():
    if graph_dict.__contains__('yeouido'):
        return graph_dict['yeouido']

    graph = nx.DiGraph()

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

    graph.add_edge(0, 1, weight=3)
    graph.add_edge(1, 2, weight=4)
    graph.add_edge(2, 3, weight=5)
    graph.add_edge(3, 4, weight=6)
    graph.add_edge(4, 5, weight=11)
    graph.add_edge(5, 6, weight=2)
    graph.add_edge(7, 8, weight=3)
    graph.add_edge(8, 9, weight=4)
    graph.add_edge(9, 10, weight=13)
    graph.add_edge(10, 11, weight=6)
    graph.add_edge(12, 13, weight=7)
    graph.add_edge(13, 14, weight=9)
    graph.add_edge(14, 15, weight=10)
    graph.add_edge(15, 16, weight=14)
    graph.add_edge(16, 17, weight=11)
    graph.add_edge(17, 18, weight=10)
    graph.add_edge(1, 0, weight=3)
    graph.add_edge(2, 1, weight=4)
    graph.add_edge(3, 2, weight=5)
    graph.add_edge(4, 3, weight=6)
    graph.add_edge(5, 4, weight=11)
    graph.add_edge(6, 5, weight=2)
    graph.add_edge(8, 7, weight=3)
    graph.add_edge(9, 8, weight=4)
    graph.add_edge(10, 9, weight=13)
    graph.add_edge(11, 10, weight=6)
    graph.add_edge(13, 12, weight=7)
    graph.add_edge(14, 13, weight=9)
    graph.add_edge(15, 14, weight=10)
    graph.add_edge(16, 15, weight=14)
    graph.add_edge(17, 16, weight=11)
    graph.add_edge(18, 17, weight=10)

    graph.add_edge(1, 7, weight=13)
    graph.add_edge(2, 8, weight=5)
    graph.add_edge(3, 9, weight=7)
    graph.add_edge(4, 10, weight=8)
    graph.add_edge(5, 11, weight=3)
    graph.add_edge(7, 1, weight=13)
    graph.add_edge(8, 2, weight=5)
    graph.add_edge(9, 3, weight=7)
    graph.add_edge(10, 4, weight=8)
    graph.add_edge(11, 5, weight=3)

    graph.add_edge(7, 13, weight=5)
    graph.add_edge(8, 14, weight=7)
    graph.add_edge(9, 15, weight=2)
    graph.add_edge(10, 16, weight=9)
    graph.add_edge(11, 17, weight=3)
    graph.add_edge(13, 7, weight=5)
    graph.add_edge(14, 8, weight=7)
    graph.add_edge(15, 9, weight=2)
    graph.add_edge(16, 10, weight=9)
    graph.add_edge(17, 11, weight=3)

    graph.add_edge(6, 18, weight=8)
    graph.add_edge(18, 6, weight=8)

    node_idx = make_node_idx(node)
    graph_dict['yeouido'] = (node, node_idx, graph)
    return graph_dict['yeouido']


def get_rectangle_graph():
    if graph_dict.__contains__('rectangle'):
        return graph_dict['rectangle']

    graph = nx.DiGraph()

    node = {
        0: (0, 0),
        1: (0, 2),
        2: (2, 2),
        3: (2, 0),
    }

    graph.add_edge(0, 1, weight=1)
    graph.add_edge(1, 2, weight=1)
    graph.add_edge(2, 3, weight=1)
    graph.add_edge(3, 0, weight=1)

    graph.add_edge(1, 0, weight=1)
    graph.add_edge(2, 1, weight=1)
    graph.add_edge(3, 2, weight=1)
    graph.add_edge(0, 3, weight=1)

    node_idx = make_node_idx(node)
    graph_dict['rectangle'] = (node, node_idx, graph)
    return graph_dict['rectangle']


def get_grid_graph():
    if graph_dict.__contains__('grid'):
        return graph_dict['grid']

    random.seed(0)
    graph = nx.DiGraph()

    node = {}

    idx = 0
    for i in [0, 5, 10, 15, 20]:
        for j in [0, 5, 10, 15, 20]:
            node[idx] = (i, j)
            idx += 1

    for i in range(5):
        for j in range(4):
            # print(5 * i + j, 5 * i + j + 1)
            graph.add_edge(
                5 * i + j,
                5 * i + j + 1,
                weight=random.randint(
                    1,
                    4))
            graph.add_edge(
                5 * i + j + 1,
                5 * i + j,
                weight=random.randint(
                    1,
                    4))

    for i in range(5):
        for j in range(4):
            # print(5 * j + i, 5 * (j + 1) + i)
            graph.add_edge(5 * j + i, 5 * (j + 1) + i,
                           weight=random.randint(1, 4))
            graph.add_edge(5 * (j + 1) + i, 5 * j + i,
                           weight=random.randint(1, 4))

    nx.draw(graph)

    node_idx = make_node_idx(node)
    graph_dict['grid'] = (node, node_idx, graph)
    return graph_dict['grid']
