#!/usr/bin/python

from mininet.topo import Topo
import pickle

class CustomTopologyInitializer( Topo ):
	"Create custom topo."

	def __init__(self, networkFileName):

		# Initialize topology
		Topo.__init__( self )

		self.myHosts = list()
		
		# Add hosts and switches
		switches = dict()
		network = pickle.load(open(networkFileName, "rb"))
		for v in network['V_P']:
			switches[v] = self.addSwitch("s" + str(v))
			if v in network['V_L']:
				host = self.addHost("h" + str(v))
				self.myHosts.append(host)
				self.addLink(host, switches[v])

		# Add links
		for (u,v) in network['E_P']:
			self.addLink(switches[u], switches[v])
		
		#print "**** Switches ****"
		#print switches
