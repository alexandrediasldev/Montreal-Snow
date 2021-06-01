def load_route(file):
    route = []
    f = open(file, "r")
    with open(f) as fp:
        for line in enumerate(fp):
            route.append(line)
