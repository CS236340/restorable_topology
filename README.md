# Implementing a restorable logical topology

This project is an attempt to implement the MM-SRLG algorithm presented in the paper "Restorable Logical Topology in the Face of No or Partial Traffic Demand Knowledge" by Prof. Reuven Cohen and Dr. Gabi Nakibly.

There are two main components:

1. An implementation of a remote controller application, either:
 * based on the MM-SRLG algorithm.
 * based on a customized algorithm that uses disjoint paths to find routes between logical nodes.
2. A Mininet topology initializer, which receives a network description file and starts up the network in Mininet. The remote controller application also needs this file for the initialization phase.

**Network description file:**

Using Python, you will need to define a dictionary with 5 key-value pairs and then serialize it into a file using the *pickle* module:

1. 'V_P': a list of optical swithces (physical nodes).
2. 'V_L': a sublist of V_P that can serve as routers (logical nodes).
3. 'E_P': a list of optical links (physical edges).
4. 'B': an integer representing the budget of the network. The budget is the maximum number of logical links allowed.
5. 'C_P': an integer representing the capacity of each link in the network. It must be even and greater or equal to 2.

See examples in the directory *network_generators*.

**Starting up the controller:**

Run the following command from Ryu's main directory (modify the paths in the command accordingly):
> PYTHONPATH=. ./bin/ryu-manager ../restorable_topology/remote_controller_apps/MM_SRLG_Controller.py --project-network-file ../restorable_topology/test_results/grid/grid1.p --observe-links

**Starting Mininet:**

First, you will need to edit the file *restorable_topology/src/mininet/customTopologyInitializerTest.py*. The instantiation of the object CustomTopologyInitializer receives a string representing a path to a file. Here you need to type the path to the network description file, the same file that was given to the "--project-network-file" switch in the command above.

Then run the following command:
> mn --custom restorable_topology/src/mininet/customTopologyInitializerTest.py --topo customTopology --controller=remote --switch ovsk --mac --arp

This project has been tested with RYU version 4.2.
