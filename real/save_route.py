def save_route(route, file):
    f = open(file, "w")
    for e in route:
        f.write(str(e) + '\n')
    f.close()
