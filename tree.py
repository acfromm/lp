import networkx as nx

def binary_tree(height, row=0, col=0):
    root = (row, col)
    if height > 0:
        T1 = binary_tree(height-1, row=row+1, col=2*col)
        T2 = binary_tree(height-1, row=row+1, col=2*col+1)
        T = nx.union(T1, T2)
        T.add_edges_from([(root, (row+1, 2*col)), (root, (row+1, 2*col+1))])
    else:
        T = nx.DiGraph()
        T.add_node(root)
    return T

print(binary_tree(10).edges)
