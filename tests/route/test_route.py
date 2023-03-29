from entity import Location
from graph.route import find_route, convert_route_tuple, find_graph_route, get_map


def test_find_route():
    assert convert_route_tuple(find_route(
        Location(0, 0), Location(0, 10))) == [(0, 10)]
    assert convert_route_tuple(find_route(Location(0, 3), Location(5, 2))) == [
        (5, 3), (5, 2)]
    assert convert_route_tuple(
        find_route(
            Location(
                10, 4), Location(
                5, 7))) == [
        (5, 4), (5, 7)]
    assert convert_route_tuple(find_route(
        Location(4, 4), Location(4, 4))) == [(4, 4)]
    assert convert_route_tuple(find_route(Location(2, 2), Location(1, 1))) == [
        (1, 2), (1, 1)]


def test_find_route_graph():
    graph_name = 'rectangle'
    node, node_idx, graph = get_map(graph_name)

    route = find_graph_route(graph_name, Location(
        node[0][0], node[0][1]), Location(node[2][0], node[2][1]))

    assert (route[0].depart_loc.x, route[0].depart_loc.y) == (0, 0)
    assert (route[0].arrive_loc.x, route[0].arrive_loc.y) == (0, 2)
    assert route[0].weight == 1

    assert (route[1].depart_loc.x, route[1].depart_loc.y) == (0, 2)
    assert (route[1].arrive_loc.x, route[1].arrive_loc.y) == (2, 2)
    assert route[1].weight == 1
