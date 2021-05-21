

def init_mat(n, edges, op_plus, e_plus, op_times, e_times):
  # Set up the matrix
  M = [[e_plus for _ in range(n)] for _ in range(n)]
  # Matrix for the successors of each vertex
  Succ = [[None for _ in range(n)] for _ in range(n)]

  # Diag elems
  for i in range(n):
    M[i][i] = e_times
    Succ[i][i] = i

  # Add the edges
  for (a,b,w) in edges:
    M[a][b] = w
    Succ[a][b] = b

  return M, Succ

def path(Succ, i, j):
  assert len(Succ) == len(Succ[0])
  assert (0 <= i < len(Succ)) and (0 <= j < len(Succ))

  if Succ[i][j] is None:
    return []

  path = [i]
  while i != j:
    i = Succ[i][j]
    path.append(i)
  return path

def floyd_warshall(n, edges, op_plus, e_plus, op_times, e_times):
  # Generalised Floyd-Warshall algorithm
  # with successor computation

  M_last, Succ = init_mat(n, edges, op_plus, e_plus, op_times, e_times)

  # Floyd-Warshall triple loop
  for k in range(n):
    M_current = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
      for j in range(n):
        M_current[i][j] = op_plus(M_last[i][j], op_times(M_last[i][k], M_last[k][j]))
        # Check if changed
        if M_current[i][j] != M_last[i][j]:
          Succ[i][j] = Succ[i][k]
    M_last = M_current

  return M_current, Succ