from ALG import ALG
import math
import random

def MM_SRLG_arb(graph, V_L, B):
    graph_copy = graph.copy()
    C = 1
    ALG_returnValue = (0, dict())
    while (C <= math.ceil(B/2)):
        for u,v in graph_copy.edges():
            graph_copy[u][v]['weight'] = min(2*C, graph[u][v]['weight'])
        ALG_returnValue = ALG(graph_copy, V_L)
        if  ALG_returnValue[0] >= B:
            break
        C = C+1
    if (len(ALG_returnValue[1].keys()) <= B):
        return ALG_returnValue[1]
    else:
        newDictionary = dict()
        keys = random.sample(ALG_returnValue[1].keys(),B)
        for k in keys:
            newDictionary[k] = (ALG_returnValue[1])[k]
        return newDictionary
