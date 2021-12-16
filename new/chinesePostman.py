import networkx as nx
import itertools

edges = [[5, 7], [1, 5], [0, 1], [7, 6], [2, 3], [4, 5], [2, 6], [0, 2], [7, 3], [6, 4], [4, 0], [3, 1]]

g = nx.Graph()
for i in edges:
    g.add_edge(i[0],i[1])

nodes_odd_degree  = (v for v, d in g.degree() if d % 2 == 1)
odd_node_pairs = list(itertools.combinations(nodes_odd_degree, 2))

def get_path_distances(graph, pairs):
    """Compute shortest distance between each pair of nodes in a graph.  Return a dictionary keyed on node pairs (tuples)."""
    distances = {}
    for pair in pairs:
        distances[pair] = nx.dijkstra_path_length(graph, pair[0], pair[1])
    return distances

odd_node_pairs_shortest_paths = get_path_distances(g, odd_node_pairs)

def create_complete_graph(pair_weights, flip_weights=True):
    """
    Create a completely connected graph using a list of vertex pairs and the shortest path distances between them
    Parameters: 
        pair_weights: list[tuple] from the output of get_shortest_paths_distances
        flip_weights: Boolean. Should we negate the edge attribute in pair_weights?
    """
    g = nx.Graph()
    for k, v in pair_weights.items():
        wt_i = - v if flip_weights else v
        # g.add_edge(k[0], k[1], {'distance': v, 'weight': wt_i})  # deprecated after NX 1.11 
        g.add_edge(k[0], k[1], **{'distance': v, 'weight': wt_i})  
    return g

g_odd_complete = create_complete_graph(odd_node_pairs_shortest_paths, flip_weights=True)

odd_matching_dupes = nx.algorithms.max_weight_matching(g_odd_complete, True)


naive_euler_circuit = list(nx.eulerian_circuit(g, source=0))

for i in naive_euler_circuit:
    print(i)