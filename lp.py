import matplotlib.pyplot as plt
import networkx as nx
import random as rand

G = nx.Graph()
nodes = ((i, {'pos': (rand.random(), rand.random())}) for i in range(10))
G.add_nodes_from(nodes)
edges = rand.sample([(u, v) for u in G.nodes for v in G.nodes if u < v], 20)
G.add_edges_from(edges)
nx.draw(G, pos={v: data['pos'] for v, data in G.nodes(data=True)})
plt.show()
