import numpy as np
import scipy.sparse
import networkx as nx


def closeness_centrality(G):
    A = nx.adjacency_matrix(G).tolil()
    D = scipy.sparse.csgraph.floyd_warshall(
        A, directed=False, unweighted=False)
    n = D.shape[0]
    closeness_centrality = {}
    nodes = list(G.nodes())  # Get a list of all node names
    for r in range(0, n):
        cc = 0.0
        possible_paths = list(enumerate(D[r, :]))
        shortest_paths = dict(filter(
            lambda x: not x[1] == np.inf, possible_paths))

        total = sum(shortest_paths.values())
        n_shortest_paths = len(shortest_paths) - 1.0
        if total > 0.0 and n > 1:
            s = n_shortest_paths / (n - 1)
            cc = (n_shortest_paths / total) * s
        closeness_centrality[nodes[r]] = cc  # Use node name as key
    return closeness_centrality
