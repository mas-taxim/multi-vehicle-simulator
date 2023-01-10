from object.Location import Location
from route.route import find_route, convert_route_tuple


def test_find_route():
    assert convert_route_tuple(find_route(Location(0, 0), Location(0, 10))) == [(0, 10)]
    assert convert_route_tuple(find_route(Location(0, 3), Location(5, 2))) == [(5, 3), (5, 2)]
    assert convert_route_tuple(find_route(Location(10, 4), Location(5, 7))) == [(5, 4), (5, 7)]
    assert convert_route_tuple(find_route(Location(4, 4), Location(4, 4))) == [(4, 4)]
    assert convert_route_tuple(find_route(Location(2, 2), Location(1, 1))) == [(1, 2), (1, 1)]
