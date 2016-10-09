import networkx as nx
from GridPrinter import printGirdGraph

def MM_SRLG_cycle(graph, V_L):
    spanning_tree = nx.minimum_spanning_tree(graph.copy())
    stripLeavesThatAreNotRouters(spanning_tree, V_L)
    #printGirdGraph(spanning_tree, 7, V_L, 2)
    newGraph = connectLeavesWithSecondaryPaths(graph, spanning_tree)

    logical_links = getLogicalLinks(spanning_tree, V_L)

    physical_paths = dict()
    for (u,v) in logical_links:
        firstPath = convertPathToListOfEdges(nx.shortest_path(spanning_tree, u, v))
        newGraph.remove_edges_from(firstPath)
        try:
            secondPath = convertPathToListOfEdges(nx.shortest_path(newGraph, u, v))
        except:
            secondPath = []
        newGraph.add_edges_from(firstPath)
        physical_paths[(u,v)] = [firstPath, secondPath]

    return physical_paths

def stripLeavesThatAreNotRouters(tree, V_L):
    allLeavesAreRouters = False
    while (not allLeavesAreRouters):
        allLeavesAreRouters = True
        for v in tree.nodes():
            if tree.degree(v)==1 and v not in V_L:
                #Current node is a leaf and is not a router
                allLeavesAreRouters = False
                tree.remove_node(v)

def connectLeavesWithSecondaryPaths(graph, spanning_tree):
    leaves = getLeaves(spanning_tree)
    updatedGraph = spanning_tree.copy()
    handledPairs = list()
    for u in leaves:
        for v in leaves:
            if u==v or ((v,u) in handledPairs):
                continue
            handledPairs.append((u,v))

            #check if a secondary path already exists between u and v
            shortestPathInTree = nx.shortest_path(spanning_tree, u, v)
            updatedGraphTmp = updatedGraph.copy()
            updatedGraphTmp.remove_edges_from(convertPathToListOfEdges(shortestPathInTree))
            if (nx.has_path(updatedGraphTmp, u, v)):
                continue

            #if not, then try to add a secondary path
            tmpGraph = graph.copy()
            tmpGraph.remove_edges_from(convertPathToListOfEdges(shortestPathInTree))
            try:
                secondaryShortestPath = nx.shortest_path(tmpGraph, u, v)
                updatedGraph.add_nodes_from(secondaryShortestPath)
                updatedGraph.add_edges_from(convertPathToListOfEdges(secondaryShortestPath))
            except:
                continue
    return updatedGraph

def getLeaves(tree):
    leaves = list()
    for v in tree.nodes():
            if tree.degree(v)==1:
                leaves.append(v)
    return leaves

def convertPathToListOfEdges(path):
    pathAsListOfEdges = []
    for i in range(1,len(path)):
        pathAsListOfEdges.append((path[i-1],path[i]))
    return pathAsListOfEdges

def getLogicalLinks(spanning_tree, V_L):
    DFS_nodes = list(nx.dfs_preorder_nodes(spanning_tree))
    for v in list(DFS_nodes):
        if v not in V_L:
            DFS_nodes.remove(v)
    logical_links = []
    for i in range(0,len(DFS_nodes)):
        logical_links.append((DFS_nodes[i],DFS_nodes[(i+1)%len(DFS_nodes)]))
    return logical_links
