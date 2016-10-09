from ryu.base import app_manager
from ryu.controller import mac_to_port, ofp_event
from ryu.controller.handler import set_ev_cls, MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.ofproto import ofproto_v1_0
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet, ethernet, ether_types
import ryu.app.ofctl.api as api
from ryu.topology import event
from ryu import cfg

import networkx as nx
import pickle
import operator

import sys
sys.path.append("/home/mininet/GUEST_SHARE/restorable_topology/src/main")
from GridPrinter import printGirdGraph

class ProjectController(app_manager.RyuApp):
    
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
		super(ProjectController, self).__init__(*args, **kwargs)
		self.mac_to_port = {}
		self.topology_api_app = self
		CONF = cfg.CONF
		network_description = pickle.load(open(CONF['project']['network_file'], "rb"))

		G = nx.Graph()
		G.add_nodes_from(network_description['V_P'])
		weightedEdges = []
		for (u,v) in network_description['E_P']:
			weightedEdges.append((u,v,network_description['C_P']))
		G.add_weighted_edges_from(weightedEdges)

		undirected_graph = nx.Graph()
		undirected_graph.add_nodes_from(network_description['V_P'])

		self.handledPairs = list()
		self.pairToPaths = dict()
		self.budget = network_description['B']
		self.V_L = network_description['V_L']
		#Finding first paths
		for u in self.V_L:
			for v in self.V_L:
				if u == v or (v,u) in self.handledPairs or nx.has_path(undirected_graph,u,v):
					continue
				try:
					firstPath = self.convertPathToListOfEdges(nx.shortest_path(G, u, v))
				except:
					continue
				self.handledPairs.append((u,v))
				for (x,y) in firstPath:
					G[x][y]['weight'] -= 1
					if G[x][y]['weight'] == 0:
						G.remove_edge(x,y)
				undirected_graph.add_edges_from(firstPath)
				self.pairToPaths[(u,v)] = list()
				self.pairToPaths[(u,v)].append(firstPath)
				self.budget -= 1

		#printGirdGraph(undirected_graph, 7, network_description['V_L'], 2)
		#printGirdGraph(G, 7, network_description['V_L'], 2)

		#Finding disjoint paths
		while self.budget > 0:
			for (u,v) in self.handledPairs:
				if self.budget == 0:
					break
				for path in self.pairToPaths[(u,v)]:
					G.remove_edges_from(path)
				try:
					newPath = self.convertPathToListOfEdges(nx.shortest_path(G,u,v))
					for (x,y) in newPath:
						G[x][y]['weight'] -= 1
						if G[x][y]['weight'] == 0:
							G.remove_edge(x,y)
					undirected_graph.add_edges_from(newPath)
					self.pairToPaths[(u,v)].append(newPath)
				except:
					pass #do nothing
				for path in self.pairToPaths[(u,v)]:
					G.add_edges_from(path)
				self.budget -= 1

		#printGirdGraph(undirected_graph, 7, network_description['V_L'], 2)
		#printGirdGraph(G, 7, network_description['V_L'], 2)

		self.net = undirected_graph.to_directed()
		for v in network_description['V_L']:
			self.net.add_node("h" + str(v))
			self.net.add_edge("h" + str(v), v)
			self.net.add_edge(v, "h" + str(v))
		self.shortestPaths = dict()
		self.ourAlgoGraph = self.net.copy()
		self.ourAlgoGraph.mac_to_port = {}
		self.removedEdges = list()
		#print "**********List of nodes"
		#print self.net.nodes()
		#print "**********List of links"
		#print self.net.edges()
		#print "**********List of pairToPaths.keys()"
		#print self.pairToPaths.keys()

    def convertPathToListOfEdges(self, path):
        pathAsListOfEdges = []
        for i in range(1,len(path)):
            pathAsListOfEdges.append((path[i-1],path[i]))
        return pathAsListOfEdges

    def add_flow(self, datapath, in_port, dst, actions):
        ofproto = datapath.ofproto

        match = datapath.ofproto_parser.OFPMatch(
            in_port=in_port, dl_dst=haddr_to_bin(dst))

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
        datapath.send_msg(mod)

    def del_flow(self, datapath):
        try:
            empty_match = datapath.ofproto_parser.OFPMatch()
        except:
            return
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        mod = parser.OFPFlowMod(datapath=datapath,
                                command=ofproto.OFPFC_DELETE,
                                match=empty_match)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = msg.in_port

        if src not in self.ourAlgoGraph:
            self.ourAlgoGraph.add_node(src)
            self.ourAlgoGraph.add_edge(dpid, src, {'port':msg.in_port})
            self.ourAlgoGraph.add_edge(src, dpid, {'port':0})
            self.logger.info("Packet in %s %s %s %s", dpid, src, dst, msg.in_port)

        if eth.ethertype == ether_types.ETH_TYPE_IPV6 or eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore ipv6 packet
            return

        if dst in self.ourAlgoGraph:
            self.logger.info("Packet at %s, from src %s to dst %s through port %s", dpid, src, dst, msg.in_port)
            try:
                path = self.shortestPaths[(src, dst)]
            except KeyError:
                copiedGraph = self.ourAlgoGraph.copy()
                while True:
                    legalPath = True	
                    path = nx.shortest_path(copiedGraph, src, dst)
                    pathAsEdges = self.convertPathToListOfEdges(path)
                    pathAsEdges = pathAsEdges[1:(len(pathAsEdges)-1)]
                    for edge in self.removedEdges:
                        if edge in pathAsEdges:
                            legalPath = False
                            #print "edge ", edge, " is in path ", path
                            #print "calculating a different path..."
                    if legalPath == True:
                        break;
                    copiedGraph.remove_edges_from(pathAsEdges)
                self.shortestPaths[(src, dst)] = path
            #print "path: ", path
            next = path[path.index(dpid)+1]
            #print("dpid: " + str(dpid))
            #print("next: " + str(next))
            out_port = self.ourAlgoGraph[dpid][next]['port']
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, msg.in_port, dst, actions)

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions)
        datapath.send_msg(out)

    @set_ev_cls(event.EventLinkAdd)
    def get_link_data(self, ev):
        #print "EventLinkAdd"
        self.ourAlgoGraph.add_edge(ev.link.src.dpid, ev.link.dst.dpid, {'port':ev.link.src.port_no})
        self.ourAlgoGraph.add_edge(ev.link.dst.dpid, ev.link.src.dpid, {'port':ev.link.dst.port_no})
        #print "src.dpid: ", ev.link.src.dpid, ", dst.dpid: ", ev.link.dst.dpid, ", port_no: ", ev.link.src.port_no
        #print("---------------------------------")
        self.shortestPaths.clear()

    @set_ev_cls(event.EventLinkDelete)
    def _event_link_delete_handler(self, ev):
		'''
		print "EventLinkDelete detected"
		print("---------------------------------")
		edgeAppearances = dict()
		maxAppearance = 1
		for (u,v) in self.shortestPaths.keys():
			for (x,y) in self.convertPathToListOfEdges(self.shortestPaths[(u,v)]):
				try:
					edgeAppearances[(x,y)] += 1
					if edgeAppearances[(x,y)] > maxAppearance:
						maxAppearance = edgeAppearances[(x,y)]
				except:
					try:
						edgeAppearances[(y,x)] += 1
						if edgeAppearances[(y,x)] > maxAppearance:
							maxAppearance = edgeAppearances[(y,x)]
					except:
						edgeAppearances[(x,y)] = 1
		print "max edge appearance is: ", maxAppearance, "of edges:"
		for (u,v) in edgeAppearances.keys():
			if edgeAppearances[(u,v)] == maxAppearance:
				print (u,v)
		sorted_edgeAppearances = sorted(edgeAppearances.items(), key=operator.itemgetter(1))
		print "edgeAppearances: ", sorted_edgeAppearances
		'''
		src_dpid = ev.link.src.dpid
		dst_dpid = ev.link.dst.dpid
		self.removedEdges.append((src_dpid, dst_dpid))
		self.shortestPaths.clear()

    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def _port_state_change_handler(self, ev):
        #print "EventOFPPortStatus detected"
        msg = ev.msg
        datapath = msg.datapath

        for dpid in self.mac_to_port.keys():
            datapath=api.get_datapath(self,dpid)
            self.del_flow(datapath)	
            del self.mac_to_port[dpid]
            self.mac_to_port.setdefault(dpid, {})

