#!/usr/bin/python

import sys
sys.path.append("/home/mininet/GUEST_SHARE/restorable_topology/src/mininet")

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
import time
from customTopologyInitializer import CustomTopologyInitializer

def iperfBetweenHosts(net, listOfHosts):
	sum = 0
	count = 0
	for src in listOfHosts:
		for dst in listOfHosts:
			if src == dst:
				continue
			count += 1
			srcHost = net.getNodeByName(src)
			dstHost = net.getNodeByName(dst)
			iperfResult = net.iperf(hosts=[srcHost, dstHost])
			print "number: ", float((iperfResult[0].split(' '))[0])
			sum += float((iperfResult[0].split(' '))[0])
	print "Average speed: ", sum/count

def BandwidthTest():
	topo = CustomTopologyInitializer("../../test_results/grid/grid1.p")
	net = Mininet(topo=topo, controller=RemoteController, switch=OVSKernelSwitch, autoSetMacs=True, autoStaticArp=True)
	net.start()
	waitingTime = 20
	print "*** Waiting for ", waitingTime, " seconds ***"
	time.sleep(waitingTime)
	net.pingAll()
	iperfBetweenHosts(net, topo.myHosts)
	net.configLinkStatus("s18", "s20", "down")
	net.pingAll()
	iperfBetweenHosts(net, topo.myHosts)
	net.stop()

print( "*** Running BandwidthTest ***")
BandwidthTest()
