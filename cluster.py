from matplotlib import pyplot as plt
import csv
import networkx as nx
import networkx.algorithms.community.centrality as gn
import os
import sys

# install faker
# pip install faker
from faker import Factory
from collections import defaultdict
from networkx import edge_betweenness_centrality as betweenness


import matplotlib.pyplot as plt
import itertools

def create_graph(filename):
    try:


        print("inside create graph")
        data = []
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile)
            #next(readCSV)
            next(readCSV)
            for i in readCSV:
                #print(i[1],i[2])
                data.append((i[1],i[2]))
            #print(data)
                
                #print(i)
                #if(l!=['Text', '', '']):
                #    data.append((l[1],l[2]))

        #print(data)

        G = nx.Graph()
        for values in data:
            u_username = values[0] # 0 has username
            v_location = values[1] # 1 has location

            G.add_edge(u_username,v_location)   # create an edge between location and username

        #print(data)
        #print(G.edges())
        #nx.draw(G)
        return G
    except:
        print("***************************************************************************\n")
        print("Kindly run the collect.py file by entering ---->  ' 2 '   to download the data for clustering")
        print("***************************************************************************\n")
        sys.exit()
        #***********************
    '''
    print("\nCreated graph from data in file --> " + filename+"\n")
    print("\nGraph Contains : ")
    print("----------------")
    print("\n " + str(len(G.nodes())) + " Nodes")
    print("\n " + str(len(G.edges())) + " Edges")
    return G
    '''
def saveGraph(G):

    pos = nx.spring_layout(G, scale=5)
    
    plt.axis("off")
    
    nx.draw_networkx_nodes(G, pos, alpha=0.5, node_size=20, node_color='blue')
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.4)
    plt.savefig("Cluster_Folder"+os.path.sep+"Graph.png", dpi=400)
    print("\nSaved Graph before Clustering to --> Graph.png in the Cluster_Folder")

def graphClusters(G,k):

    comp = girvan_newman(G)
    # print(tuple(sorted(c) for c in next(comp)))

    result = tuple
    for comp in itertools.islice(comp, k-1):

        result = tuple(sorted(c) for c in comp)

    return result

def girvan_newman(G, most_valuable_edge=None):


    if G.number_of_edges() == 0:
        yield tuple(nx.connected_components(G))
        return

    if most_valuable_edge is None:
        def most_valuable_edge(G):
            betweenness = nx.edge_betweenness_centrality(G)
            return max(betweenness, key=betweenness.get)
    g = G.copy().to_undirected()
    g.remove_edges_from(g.selfloop_edges())

    while g.number_of_edges() > 0:
        
        yield minimum_central_edges(g, most_valuable_edge)
        
#.>>>down called
def minimum_central_edges(G, most_valuable_edge):

    original_num_components = nx.number_connected_components(G)
    num_new_components = original_num_components
    new_components = tuple()
    while num_new_components <= original_num_components:
        edge = most_valuable_edge(G)
        G.remove_edge(*edge)
        new_components = tuple(nx.connected_components(G))
        num_new_components = len(new_components)
    return new_components

def unique_users(list1): 
  
    # intilize a null list 
        unique_list = [] 
      
    # traverse for all elements 
        for x in list1: 
            if x not in unique_list: 
                unique_list.append(x) 
        return unique_list


def saveClusters(cluster_tup):


    


    with open("Cluster_Folder"+os.path.sep+"cluster.txt",'w') as fp:
        
        for i in range(len(cluster_tup)):
            
            fp.write("Cluster " + str(i) + str(cluster_tup[i]) + "\n")

    fp.close()
    print("\nClusters are saved to --> " + "cluster.txt in Cluster_Folder folder\n")
    
def cluster_details(Communities_tuple):
    """
    This saves the details of the clusters found and saves it to the cluster_details.txt file in the Clusters_Folder

    """

    unq = []
    messages = []
    labels = []
    positive_tweets = []
    negative_tweets = []
    neutral_tweets = []
    #print("No of Communities = ", len(communities))
    with open("Cluster_Folder"+os.path.sep+"cluster_testData"+".csv",'r') as f:
        f = csv.reader(f)
        next(f)
        for i in f:
            messages.append(i[0])
            unq.append(i[3])
    
    
    list_of_unique_users = []
    list_of_unique_users = unique_users(unq)

    #wtr = csv.writer(open ('summarize_cluster.txt', 'w'), delimiter=',', lineterminator='\n')
    total_users = len(list_of_unique_users)


    com_dict = defaultdict(list)

    for i in range(len(Communities_tuple)):
        com_dict[i] = Communities_tuple[i]

    totalsum = 0.0
    n_com = len(com_dict)
    for key in com_dict:
        totalsum += len(com_dict[key])

    avg_users = totalsum/n_com

    with open("Cluster_Folder"+os.path.sep+"cluster_details.txt",'w') as fp:
        fp.write("Total unique users :" +str(total_users)+"\n\n")
        fp.write("Number of communities discovered : " + str(len(Communities_tuple))+ "\n\n")
        fp.write("Average Number of users per community : " + str(avg_users)+ "\n\n")
        

    fp.close()
    return com_dict

def color_creation(no_of_communities):

    color_list = []
    fake  = Factory.create()
    for i in range(no_of_communities):
        color_list.append(fake.hex_color())

    return color_list
def save_clustered_graph(G,com_dict,color_list):

    node_color = []
    new_G = G.copy()

    for n in new_G.nodes():
        for key in com_dict:
            if n in com_dict[key]:
                node_color.append(color_list[key])

    plt.clf()
    pos = nx.spring_layout(new_G, scale=8)
    plt.axis("off")
    nx.draw_networkx_nodes(new_G, pos, alpha=0.5, node_size=20, node_color=node_color)
    nx.draw_networkx_edges(new_G, pos, alpha=0.3, width=0.4)
    plt.savefig("Cluster_Folder"+os.path.sep+"clusteredGraph.png", dpi=300)
    print("❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂")
    print("\n ❂❂❂❂ Graph..... saved in Cluster_folder ❂❂❂❂")
    print("❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂")

def main():

    G = create_graph("Cluster_Folder"+os.path.sep+"cluster_testData.csv") #"Cluster_Folder"+os.path.sep+"cluster_testData"+".csv"
    saveGraph(G=G)
    cluster_tup = graphClusters(G=G,k=7)
    print("Making K = 7 clusters graph")
    print("❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂\n")
    print("\t We are establishing the major cities from where the three candidates \n1. Donald Trump \n2.Hillary Clinton \n3. Michelle Obama \n get the major Support from.")
    print("❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂")
    
    saveClusters(cluster_tup)
    com_dict = cluster_details(Communities_tuple=cluster_tup)
    color_list = color_creation(no_of_communities=len(com_dict))
    save_clustered_graph(G=G,com_dict=com_dict,color_list=color_list)

    


if __name__ == main():
    main()


