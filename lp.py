import math
import matplotlib.pyplot as plt
import networkx as nx
import random as rand
import scipy.spatial as space

points = {i: (rand.random(), rand.random()) for i in range(10)}

def weighted_edge(u, v):
    x1, y1 = points[u]
    x2, y2 = points[v]
    return u, v, math.hypot(x2 - x1, y2 - y1)

def triangle_edges(triangle):
    indices = [(0, 1), (1, 2), (2, 0)]
    return (weighted_edge(triangle[i], triangle[j]) for i, j in indices)

G = nx.Graph()
G.add_nodes_from((v, {'pos': p}) for v, p in points.items())
for triangle in space.Delaunay(list(points.values())).simplices:
    G.add_weighted_edges_from(triangle_edges(triangle))
mst = set(nx.minimum_spanning_tree(G).edges)
edgelist = list(G.edges)
edge_color = [('red' if edge in mst else 'black') for edge in edgelist]
nx.draw_networkx(
    G, pos=points, edgelist=edgelist,
    node_color='white', edge_color=edge_color
)
plt.axis('equal')
plt.show()
