# USAir97 Complex Network Analysis

# Dataset
The USAir97 dataset which contains the list of all US Air flights in 1997 as an undirected weighted graph linking airports connected by US Air at that time. The individual airports are associated with 2D coordinates ("posx" and "posy"), the name of the corresponding city, state, and country, as well as the associated geospatial coordinates. In addition, each edge is associated with a weight that represents the frequency of the flights between the two cities. Though not huge, the dataset is fairly large from a visualization standpoint with 332 nodes (airports) and 2126 links (flights)

# Visualization of Network
Below graph is a visualization of the complex network. Thanks to the graph, we can easily discover the network and make some interpretation. First of all, there are many nodes with only one connection and they scattered around the graph. On the other hands, we can able to see nodes in the center of graph have many connections with each other. 

![USAir97](https://github.com/MuhammetEmek/USAir97_Analysis/blob/main/images/UsAir97.png)

# Network Macro Topology
Macro topological values computed by the application are shown below and have been exported as html file (Macro_Statistics.html). This network is fully connected with 332 nodes and 2126 links each other. Since the density value (0.039) is very low, this network can be considered sparse network. The degree assortativity value (-0.207876) is negative so the tendency for nodes to connect to other nodes with dissimilar degree values within a network can be occur. Low transitivity (0.396392) means that the network contains communities or groups of airports that are sparsely connected internally. According to the diameter value, the two most distant airports in the network can be reached with 6 flights. Average Betweenness Centrality value is too low, however the average Harmonic Centrality value is seen higher than others. 

![Macro](https://github.com/MuhammetEmek/USAir97_Analysis/blob/main/images/UsAir97.png)
