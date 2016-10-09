import networkx as nx
from MM_SRLG_cycle import MM_SRLG_cycle
from MM_SRLG_arb import MM_SRLG_arb
from GridPrinter import printGirdGraph

def MM_SRLG(V_P, E_P, C_P, V_L, B):
    graph = nx.Graph()
    graph.add_nodes_from(V_P)
    weightedEdges = []
    for (u,v) in E_P:
        weightedEdges.append((u,v,C_P))
    graph.add_weighted_edges_from(weightedEdges)
    E_cycle = MM_SRLG_cycle(graph, V_L)
    resultGraph = nx.Graph()
    for pathPair in E_cycle.values():
        for (u,v) in pathPair[0]:
            graph[u][v]['weight'] -= 1
        for (u,v) in pathPair[1]:
            graph[u][v]['weight'] -= 1
        resultGraph.add_edges_from(pathPair[0])
        resultGraph.add_edges_from(pathPair[1])
    #printGirdGraph(resultGraph, 7, V_L, 2)
    E_arb = MM_SRLG_arb(graph, V_L, B - len(V_L))
    for path in E_arb.values():
        resultGraph.add_edges_from(path)
    return resultGraph
