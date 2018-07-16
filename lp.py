import math
import matplotlib.pyplot as plt
import networkx as nx
import random as rand
import scipy.spatial as space

points = {i: (rand.uniform(0, 1), rand.uniform(0, 1)) for i in range(20)}

def weighted_edge(u, v):
    x1, y1 = points[u]
    x2, y2 = points[v]
    return u, v, math.hypot(x2 - x1, y2 - y1)

def triangle_edges(triangle):
    indices = [(0, 1), (1, 2), (2, 0)]
    return (weighted_edge(triangle[i], triangle[j]) for i, j in indices)

def shortest_path_tree(G, source):
    predecessors, _ = nx.dijkstra_predecessor_and_distance(G, source)
    edges = (weighted_edge(u, v) for u, vs in predecessors.items() for v in vs)
    T = nx.Graph()
    T.add_weighted_edges_from(edges)
    return T

def color(x, s1, s2):
    if x in s1:
        return 'purple' if x in s2 else 'red'
    else:
        return 'blue' if x in s2 else 'black'

G = nx.Graph()
G.add_nodes_from((v, {'pos': p}) for v, p in points.items())
for triangle in space.Delaunay(list(points.values())).simplices:
    G.add_weighted_edges_from(triangle_edges(triangle))
edgelist = list(G.edges)
mst = nx.minimum_spanning_tree(G)
spt = shortest_path_tree(G, 0)
print('MST weight:', mst.size(weight='weight'))
print('SPT weight:', spt.size(weight='weight'))
print()
print('MST paths:', sum(nx.single_source_dijkstra_path_length(mst, 0).values()))
print('SPT paths:', sum(nx.single_source_dijkstra_path_length(spt, 0).values()))
mst_edges, spt_edges = (set(map(frozenset, T.edges)) for T in [mst, spt])
edge_color = [color(frozenset(edge), mst_edges, spt_edges) for edge in edgelist]
nx.draw_networkx(
    G, pos=points, edgelist=edgelist,
    node_color='white', edge_color=edge_color
)
plt.axis('equal')
plt.show()
