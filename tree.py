import gurobipy as gurobi
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

def ilp(G, k):
    dist = dict(nx.all_pairs_shortest_path_length(G))
    closure = nx.transitive_closure(G)
    candidates = {v: {v} | set(closure.predecessors(v)) for v in G.nodes}

    m = gurobi.Model()

    y = {}
    for j in G.nodes:
        y[j] = m.addVar(vtype=gurobi.GRB.BINARY)
    x = {}
    for i in G.nodes:
        for j in candidates[i]:
            x[i, j] = m.addVar(vtype=gurobi.GRB.BINARY)

    m.setObjective(sum(x[i, j] * dist[j][i] for i, j in x.keys()))

    m.addConstr(sum(y[j] for j in G.nodes) <= k)
    for i in G.nodes:
        m.addConstr(sum(x[i, j] for j in candidates[i]) == 1)
    for i, j in x.keys():
        m.addConstr(x[i, j] <= y[j])

    m.optimize()

    return [j for j in G.nodes if y[j].x > 0.5]

print(ilp(binary_tree(9), 99))
