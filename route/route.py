from object.Location import Location


def find_route(start: Location, dest: Location):
    route = []

    if start.x != dest.x:
        route.append(Location(dest.x, start.y))

    if start.y != dest.y:
        route.append(Location(dest.x, dest.y))

    if start.x == dest.x and start.y == dest.x:
        route.append(Location(dest.x, dest.y))

    return route


