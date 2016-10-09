from pulp import *

def ALG(graph, V_L):
    prob = LpProblem("MaximizeLogicalLinks", LpMaximize)

    #condition 4
    #l_u_v variables
    logical_links = dict()
    for u in V_L:
        for v in V_L:
            if u == v: continue
            if (v,u) in logical_links: continue
            logical_links[(u,v)] = LpVariable("l_%d_%d" % (u,v), 0, 1, LpBinary)
    #r_u_v_i_j variables
    logical_over_physical = dict()
    for i,j in graph.edges():
        for (u,v) in logical_links:
            logical_over_physical[(u,v,i,j)] = LpVariable("r_e_%d_%d_%d_%d" % (u,v,i,j), 0, 1, LpBinary)
            logical_over_physical[(u,v,j,i)] = LpVariable("r_e_%d_%d_%d_%d" % (u,v,j,i), 0, 1, LpBinary)
            prob += (logical_over_physical[(u,v,i,j)] + logical_over_physical[(u,v,j,i)]) <= 1

    #condition 2
    prob += lpSum(logical_links[(u,v)] for (u,v) in logical_links)

    #condition 3
    for i,j in graph.edges():
        prob += lpSum(logical_over_physical[(u,v,i,j)] for (u,v) in logical_links) <= graph[i][j]['weight']

    #condition 1
    for (u,v) in logical_links:
        for i in graph.nodes():
            edges_in = []
            edges_out = []
            for j in graph.neighbors(i):
                edges_in.append(logical_over_physical[(u,v,j,i)])
                edges_out.append(logical_over_physical[(u,v,i,j)])

            if i == u:
                prob += lpSum(edges_in) - lpSum(edges_out) == -logical_links[(u,v)]
            elif i == v:
                prob += lpSum(edges_in) - lpSum(edges_out) ==  logical_links[(u,v)]
            else:
                prob += lpSum(edges_in) - lpSum(edges_out) == 0

    prob.solve()
    #print("Status:", LpStatus[prob.status])

    # The optimised objective function value is printed to the screen
    #print("L =", value(prob.objective))

    # Each of the variables is printed with it's resolved optimum value
    #for v in prob.variables():
    #    print(v.name, "=", v.varValue)

    physical_paths = dict()
    for (u,v) in logical_links:
        if (logical_links[(u,v)].varValue == 1):
            physical_paths[(u,v)] = list()
            for i,j in graph.edges():
                if (logical_over_physical[(u,v,i,j)].varValue == 1) \
                    or (logical_over_physical[(u,v,j,i)].varValue == 1):
                    physical_paths[(u,v)].append((i,j))

    return (value(prob.objective),physical_paths)
