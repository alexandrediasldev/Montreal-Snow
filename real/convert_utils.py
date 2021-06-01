
def euler_circuit_to_route(euler_circuit):
    route = []
    for edge in euler_circuit:
        route.append(edge[0])
    return route


def route_to_long_lat(G, route):
    long = []
    lat = []
    for i in route:
        point = G.nodes[i]
        long.append(point['x'])
        lat.append(point['y'])
    return long, lat


def long_lat_to_points(long, lat):
    origin_point = long[0], lat[0]
    dest_point = long[-1], lat[-1]
    return origin_point, dest_point