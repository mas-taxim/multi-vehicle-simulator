import networkx as nx

from ..entity import Location, Path
from .map import get_map, get_hour

graph_dict = dict()
distances = []


def get_distance(graph_name, source, target):
    if len(distances) == 0:
        f = open(f'graph/data/dist_{graph_name}_{get_hour()}.csv', 'r')

        lines = f.readlines()
        for line in lines:
            distances.append(line)

        f.close()

    return float(distances[source].split(",")[target])


def get_nearest_idx(node_idx: dict, loc: Location):
    min_value = 99999999
    min_idx = -1
    for n_loc in node_idx.keys():
        if min_value > abs(loc.x - n_loc[0]) + abs(loc.y - n_loc[1]):
            min_value = abs(loc.x - n_loc[0]) + abs(loc.y - n_loc[1])
            min_idx = node_idx[n_loc]

    return min_idx


def find_graph_route(graph_name: str, start: Location, dest: Location):
    node, node_idx, graph = get_map(graph_name)

    route = []

    start_idx = node_idx[(start.x, start.y)]
    dest_idx = node_idx[(dest.x, dest.y)]

    cur_idx: int = start_idx
    for n_idx in nx.shortest_path(graph, start_idx, dest_idx, weight='weight')[1:]:
        route.append(Path(Location(node[cur_idx][0], node[cur_idx][1]),
                          Location(node[n_idx][0], node[n_idx][1]),
                          graph[cur_idx][n_idx]['weight']))
        cur_idx = n_idx

    return route


def find_route(start: Location, dest: Location):
    route = []

    next_loc = Location(start.x, start.y)

    while next_loc.x != dest.x or next_loc.y != dest.y:
        if next_loc.x != dest.x:
            route.append(Location(dest.x, next_loc.y))
            next_loc.x = dest.x
        elif next_loc.y != dest.y:
            route.append(Location(next_loc.x, dest.y))
            next_loc.y = dest.y

    if not route:
        route.append(Location(dest.x, dest.y))

    return route


def convert_route_tuple(route):
    route_list = []

    for r in route:
        route_list.append((r.x, r.y))

    return route_list
