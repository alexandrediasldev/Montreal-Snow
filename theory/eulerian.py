def degres(adj_mat):
    n = len(adj_mat)
    res = [0] * n

    for i in range(n):
        res[i] = adj_mat[i].count(1)

    return res


def is_eulerian(adjs):
    odds = degres(adjs)
    ct = 0

    for v in odds:

        if v % 2 == 0:
            ct += 1

        if ct > 2:
            return False

    return ct != 0 or ct == 2

