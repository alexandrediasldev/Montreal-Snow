def adj_list(edges, n): #adj list made from an edge list with n nodes
    successor = [[] for a in range(n)]

    for (a, b) in edges:
        successor[a].append(b)
        successor[b].append(a)

    return successor
