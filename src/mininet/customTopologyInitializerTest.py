#!/usr/bin/python

import sys
sys.path.append("/home/mininet/GUEST_SHARE/restorable_topology/src/mininet")

from customTopologyInitializer import CustomTopologyInitializer

topos = { 'customTopology': ( lambda: CustomTopologyInitializer("../../test_results/grid/grid1.p") ) }
