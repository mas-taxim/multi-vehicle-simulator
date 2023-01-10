from object.Location import Location


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
