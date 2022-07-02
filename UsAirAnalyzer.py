# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 14:59:43 2022

@author: memek
"""

import time
import json
import pandas as pd
import igraph as ig
import matplotlib.pyplot as plt
from statistics import mean
 
NETWORK_FILE_NAME = 'USAir97v2.json'
GRAPH_NODES_LABEL = 'nodes'
GRAPH_LINKS_LABEL = 'links'
LINK_SOURCE_LABEL = 'source'
LINK_TARGET_LABEL = 'target'
NODE_INFO_LABEL   = 'info'

def generate_network_graph():
    # Opening JSON file of complex graph
    json_file = open(NETWORK_FILE_NAME)
     
    # returns JSON object as a dictionary
    graph_data = json.load(json_file)
    
    # retrieving nodes
    nodes = graph_data[GRAPH_NODES_LABEL]
    
    # retrieving links
    links = graph_data[GRAPH_LINKS_LABEL]
    
    # Closing file
    json_file.close()
    
    # Preparing edges
    edges = []
    for link in links:
        edges.append([link[LINK_SOURCE_LABEL]-1,link[LINK_TARGET_LABEL]-1])
    
    # Initializing graph object with nodes and edges data
    return ig.Graph(vertex_attrs={NODE_INFO_LABEL:nodes}, edges=edges, directed=False)

def get_node_info(graph, index):
    vertex_info = graph.vs[index]['info']
    return '%-40s ( %-12s )' % (vertex_info['name'], vertex_info['state'])

def get_airport_name(graph, index):
    vertex_info = graph.vs[index]['info']
    return vertex_info['name']

def get_top_n_airport(graph, dist_list, n, is_float):
    # Finding top n id
    top_n_vertex_id_list = sorted(range(len(dist_list)), key=lambda i: dist_list[i])[-n:]
    
    # Reversing id_list
    top_n_vertex_id_list.reverse()
    airport_list = []
    format_str = '%-40s: %8.6f' if is_float else '%-40s: %3d'
    for index in top_n_vertex_id_list:
        airport_list.append(format_str % (get_airport_name(graph, index), dist_list[index]))
        
    return airport_list

def print_top_n_airport(graph, dist_list, title, n, is_float):
    format_str = '%-60s : %8.6f' if is_float else '%-60s : %3d'
    print('-----------------------------------------------------------------------')
    print('--' + title.center(67,' ') + '--')
    print('-----------------------------------------------------------------------')    
    # Finding top n id
    top_n_vertex_id_list = sorted(range(len(dist_list)), key=lambda i: dist_list[i])[-n:]
    
    # Reversing id_list
    top_n_vertex_id_list.reverse()
    for index in top_n_vertex_id_list:
        print(format_str % (get_node_info(graph, index), dist_list[index]))
        
    print('-----------------------------------------------------------------------')
    
def get_normalized_betweenness(graph):     
    betweenness  = graph.betweenness()
    graph_vcount = graph.vcount()
    return list(map(lambda x: (2 / ((graph_vcount-1) * (graph_vcount-2))) * x, betweenness))    
    
def plot_graph(graph):
    fig, ax = plt.subplots(figsize=(20, 20))    
    ig.plot(graph, target=ax)
    plt.title('USAir97 Complex Network')
    plt.show()
    
def plot_clusters(graph, clusters, title):
    color_palette = ig.drawing.colors.ClusterColoringPalette(len(clusters))
    graph.vs['color'] = color_palette.get_many(clusters.membership)
        
    fig, ax = plt.subplots(figsize=(20, 20))
    ig.plot(graph, vertex_color = graph.vs['color'], target = ax)
    plt.title(title)
    plt.show()

def plot_diameter(graph):
    diameter = []
    vertex_id_list = graph.get_diameter()
    graph_degree = graph.degree()
    for vertex_id in vertex_id_list:
        vertex_info = graph.vs[vertex_id]['info']
        diameter.append([vertex_id, vertex_info['name'], vertex_info['state'], graph_degree[vertex_id]])            
        
     # Creating dataframe
    diameter_df = pd.DataFrame(diameter, columns=['ID','Name', 'State', 'Degree'])
   
    # Printing diamer
    print('------------------------------')
    print('  Diameter (Shortest Path)    ')
    print('------------------------------')  
    print(diameter_df)        
    
    graph.vs['color'] = '#1f77b4'
    graph.vs[vertex_id_list]['color'] = '#d62728'
        
    fig, ax = plt.subplots(figsize=(20, 20))
    ig.plot(graph, vertex_color = graph.vs['color'], target = ax)
    plt.title('Diameter (Shortest Path)')
    plt.show()
        

def print_and_save_macro_statistics(graph):
    df_index = ['Number of Nodes',
    			'Number of Edges', 
    			'Is Connected?',              
    			'Density',
    			'Maximum degree',  
    			'Average degree', 
                'Minimum degree',
    			'Degree assortativity',           
    			'Number of triangles',           
    			'Transitivity',    
    			'Average local tansitivity',
                'Diameter',        
    			'Radius',  
    			'Average (geodesic) distance',   
    			'Number of Components',           
    			'Giant Component Size',      
    			'Maximum k-core',  
    			'Lower bound of Maximum Clique',
                'Betweenness Centrality',
                'Eigenvector Centrality',
                'Harmonic Centrality',
                'Closeness Centrality']

    graph_degree = graph.degree() 
    
    df_data = [(graph.vcount()),
    			graph.ecount(),
    			graph.is_connected(),
    			graph.density(),               
    			max(graph_degree),
    			mean(graph_degree),
                min(graph_degree),
    			graph.assortativity_degree(),
    			len(graph.cliques(min=3,max=3)),                
    			graph.transitivity_undirected(), #Fraction of closed triangles    
    			graph.transitivity_avglocal_undirected(mode='zero'), # Average clustering coefficient
    			graph.diameter(),
    			graph.radius(),
    			graph.average_path_length(), 
                len(graph.clusters()),
                len(max(graph.clusters())),
                max(graph.coreness()),
    			len(max(graph.largest_cliques())),
                mean(get_normalized_betweenness(graph)),
                mean(graph.eigenvector_centrality()),
                mean(graph.harmonic_centrality()),
                mean(graph.closeness())]
        
    print('-----------------------------------------')
    print('        Network Macro Statistics         ')
    print('-----------------------------------------')
    # Creating dataframe
    macro_df = pd.DataFrame(df_data, index=df_index, columns=['Value'])
   
    # Printing macro properties
    print(macro_df)
    
    # Exporting as html
    macro_df.to_html(r'Macro_Statistics.html', index = True)
    
def print_and_save_micro_statistics(graph):
    degree_list             = graph.degree()
    transitivity_local_list = graph.transitivity_local_undirected(mode='zero')
    authority_score_list    = graph.authority_score()
    hub_score_list          = graph.hub_score()
    normalized_betweenness  = get_normalized_betweenness(graph)
    eigenvector_centrality  = graph.eigenvector_centrality()
    harmonic_centrality     = graph.harmonic_centrality()
    closeness_centrality    = graph.closeness()
    
    print('-----------------------------------------')
    print('        Network Micro Statistics         ')
    print('-----------------------------------------')
    
    df_data = {
                'Degree'                 : degree_list,
                'Transitivity'           : transitivity_local_list,
                'Authority Score'        : authority_score_list,
                'Hub Score'              : hub_score_list,
                'Betweenness Centrality' : normalized_betweenness,
                'Eigenvector Centrality' : eigenvector_centrality,
                'Harmonic Centrality'    : harmonic_centrality,
                'Closeness Centrality'   : closeness_centrality                
                }        
    
    # Creating dataframe
    micro_df = pd.DataFrame(df_data)
   
    # Printing micro statistics
    print(micro_df)
    
    # Exporting as html
    micro_df.to_html(r'Micro_Statistics.html', index = True)
    
    # --------------------------------------------------------------------------------------------------------------------------------
    print('-----------------------------------------')
    print('Network Micro Statistics (Top 10 Nodes)  ')
    print('-----------------------------------------')
    
    df_data2 = {
                'Top 10 Airports by Degree'          : get_top_n_airport(graph, degree_list, 10, False),
                'Top 10 Airports by Transitivity'    : get_top_n_airport(graph, transitivity_local_list, 10, True),
                'Top 10 Airports by Authority Score' : get_top_n_airport(graph, authority_score_list, 10, True),
                'Top 10 Airports by Hub Score'       : get_top_n_airport(graph, hub_score_list, 10, True)                
                }
    
    # Creating dataframe for Distribution
    top_10_dist_df = pd.DataFrame(df_data2)
   
    # Printing top 10 nodes by Distribution
    print(top_10_dist_df)
    
    # Exporting as html
    top_10_dist_df.to_html(r'Top_10_Nodes_By_Distribution.html', index = True)
    
    df_data3 = {
            'Top 10 Airports by Betweenness Centrality' : get_top_n_airport(graph, normalized_betweenness, 10, True),
            'Top 10 Airports by Eigenvector Centrality' : get_top_n_airport(graph, eigenvector_centrality, 10, True),
            'Top 10 Airports by Harmonic Centrality'    : get_top_n_airport(graph, harmonic_centrality   , 10, True),
            'Top 10 Airports by Closeness Centrality'   : get_top_n_airport(graph, closeness_centrality  , 10, True)
            }
    
    # Creating dataframe for Centrality
    top_10_cent_df = pd.DataFrame(df_data3)
   
    # Printing top 10 nodes by Centrality
    print(top_10_cent_df)
    
    # Exporting as html
    top_10_cent_df.to_html(r'Top_10_Nodes_By_Centrality.html', index = True)
          
    
    # --------------------------------------------------------------------------------------------------------------------------------
    # Plotting histrogram of distributions
    fig, axs = plt.subplots(2,2, sharey=True, figsize=(10, 10))
    axs[0,0].hist(degree_list, bins=50, edgecolor='black')
    axs[0,0].set_title('Degree Distribution')
    axs[0,1].hist(transitivity_local_list, bins=50, edgecolor='black')
    axs[0,1].set_title('Transitivity Distribution')
    axs[1,0].hist(authority_score_list, bins=50, edgecolor='black')
    axs[1,0].set_title('Authority Score Distribution')
    axs[1,1].hist(hub_score_list, bins=50, edgecolor='black')
    axs[1,1].set_title('Hub Score Distribution')
    plt.show()
    
    # Plotting boxplot of distributions
    fig, axs = plt.subplots(2,2, sharey=True, figsize=(10, 10))
    axs[0,0].boxplot(degree_list)
    axs[0,0].set_title('Degree Distribution')
    axs[0,1].boxplot(transitivity_local_list)
    axs[0,1].set_title('Transitivity Distribution')
    axs[1,0].boxplot(authority_score_list)
    axs[1,0].set_title('Authority Score Distribution')
    axs[1,1].boxplot(hub_score_list)
    axs[1,1].set_title('Hub Score Distribution')
    plt.show()
        
    # Plotting histrogram of Centralities
    fig, axs = plt.subplots(2,2, sharey=True, figsize=(10, 10))
    axs[0,0].hist(normalized_betweenness, bins=50, edgecolor='black')
    axs[0,0].set_title('Betweenness Centrality')
    axs[0,1].hist(eigenvector_centrality, bins=50, edgecolor='black')
    axs[0,1].set_title('Eigenvector Centrality')
    axs[1,0].hist(harmonic_centrality, bins=50, edgecolor='black')
    axs[1,0].set_title('Harmonic Centrality')
    axs[1,1].hist(closeness_centrality, bins=50, edgecolor='black')
    axs[1,1].set_title('Closeness Centrality')
    fig.show()
    
    # Plotting boxplot of Centralities
    fig, axs = plt.subplots(2,2, sharey=True, figsize=(10, 10))
    axs[0,0].boxplot(normalized_betweenness)
    axs[0,0].set_title('Betweenness Centrality')
    axs[0,1].boxplot(eigenvector_centrality)
    axs[0,1].set_title('Eigenvector Centrality')
    axs[1,0].boxplot(harmonic_centrality)
    axs[1,0].set_title('Harmonic Centrality')
    axs[1,1].boxplot(closeness_centrality)
    axs[1,1].set_title('Closeness Centrality')
    fig.show()
    
    
def print_and_save_meso_statistics(graph):    
    meso_data = []
    
    # Spinglass community detection method of Reichardt & Bornholdt
    start_time = time.time()
    clusters = graph.community_spinglass()
    meso_data.append([len(clusters), usAir_graph.modularity(membership=clusters.membership), (time.time()-start_time)])
    
    plot_clusters(graph, clusters, 'Community Detection by Spinglass')
    
    # Clauset et al based on the greedy optimization of modularity
    start_time = time.time()
    clusters = graph.community_fastgreedy().as_clustering()
    meso_data.append([len(clusters), usAir_graph.modularity(membership=clusters.membership), (time.time()-start_time)])
    
    plot_clusters(graph, clusters, 'Community Detection by Fast Greedy')
        
    # The random walk method of Latapy & Pons
    start_time = time.time()
    clusters = graph.community_walktrap().as_clustering()
    meso_data.append([len(clusters), usAir_graph.modularity(membership=clusters.membership), (time.time()-start_time)])
    
    plot_clusters(graph, clusters, 'Community Detection by Walktrap')   

    # Newman's eigenvector community structure detection
    start_time = time.time()
    clusters = graph.community_leading_eigenvector()
    meso_data.append([len(clusters), usAir_graph.modularity(membership=clusters.membership), (time.time()-start_time)])
   
    plot_clusters(graph, clusters, 'Community Detection by Eigenvector')    
    
    # Infomap method of Martin Rosvall and Carl T. Bergstrom
    start_time = time.time()
    clusters = graph.community_infomap()
    meso_data.append([len(clusters), usAir_graph.modularity(membership=clusters.membership), (time.time()-start_time)])
    
    plot_clusters(graph, clusters, 'Community Detection by Infomap')
   
    # Label propagation method of Raghavan et al
    start_time = time.time()
    clusters = graph.community_label_propagation()
    meso_data.append([len(clusters), usAir_graph.modularity(membership=clusters.membership), (time.time()-start_time)])
    
    plot_clusters(graph, clusters, 'Community Detection by Label propagation')
    
    # Leiden algorithm of Traag, van Eck & Waltman
    start_time = time.time()
    clusters = graph.community_leiden()
    meso_data.append([len(clusters), usAir_graph.modularity(membership=clusters.membership), (time.time()-start_time)])
    
    plot_clusters(graph, clusters, 'Community Detection by Leiden')
           
    # Creating dataframe
    meso_df = pd.DataFrame(index=['Spinglass', 'Fast Greedy','Walktrap', 'Eigenvector','Infomap','Label_Propagation','Leiden']
                           , columns=['Community Count','Modularity','Elapsed Time'], data = meso_data)
    
    # Printing meso statistics
    print('')
    print('------------------------------------------------------------')
    print('                  Network Meso Statistics                   ')
    print('------------------------------------------------------------')
    print(meso_df)
    
    # Exporting as html
    meso_df.to_html(r'Meso_Statistics.html', index = True)
    
    
# First generate graph from Json file
usAir_graph = generate_network_graph()

# Plotting the graph
plot_graph(usAir_graph)

# Computing Network Macro Statistics
print_and_save_macro_statistics(usAir_graph)

# Computing Network Micro Statistics
print_and_save_micro_statistics(usAir_graph)

# Computing Network Meso Statistics
print_and_save_meso_statistics(usAir_graph)

# Plotting shortest path (Diameter)
plot_diameter(usAir_graph)