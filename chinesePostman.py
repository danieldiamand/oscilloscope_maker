import networkx 
from networkx.algorithms.euler import *


edges = [[5, 7], [1, 5], [0, 1], [7, 6], [2, 3], [4, 5], [2, 6], [0, 2], [7, 3], [6, 4], [4, 0], [3, 1]]



def eulerianPath(edges):
    G = networkx.Graph()
    for i in edges:
        G.add_edge(i[0],i[1])
    path = networkx.algorithms.euler.eulerian_path(networkx.algorithms.euler.eulerize(G), 0)
    return([[edge[0],edge[1]] for edge in path])

if __name__ == "__main__":
    path = (eulerianPath(edges))
    for i in path:
        print(i)
        