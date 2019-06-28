# project structure (invoking relationship)

import networkx as nx
import matplotlib.pyplot as plt
from os import path
import sys
import networkx as nx
import os
import pandas as pd


def get_project_structure(df_annotation, main_location):
    str_replace = main_location + "/"
    df_annotation['workflowName'] = df_annotation['workflowName'].str.replace(str_replace, "")
    df_annotation['invokedBy'] = df_annotation['invokedBy'].str.replace(str_replace, "")
    # Create tree object
    df_invokeWf = df_annotation.loc[:, ['workflowName', 'invokedBy']].drop_duplicates()
    # Assuming the starting xaml file is not invoked by anything else

    G = nx.from_pandas_edgelist(df_invokeWf, 'invokedBy', 'workflowName', create_using=nx.DiGraph())


    plt.figure(figsize=(15, 15))
    nx.draw(G, with_labels=True, node_size=1500, alpha=0.3, arrows=True)
    picStore = "/".join(main_location.split("/")[:-3]) + "/static/dist/chart/project_structure.png"
    count = 1
    picExists = path.isfile(picStore)
    while picExists:
        picStore = "/".join(main_location.split("/")[:-3]) + "/static/dist/chart/project_structure"+str(count)+".png"
        picExists = path.isfile(picStore)
        count += 1

    plt.savefig(picStore)
    plt.close()
    return picStore


def generate_gexf(df_annotation, main_location):

    str_replace = main_location + "/"
    df_annotation['workflowName'] = df_annotation['workflowName'].str.replace(str_replace, "")
    df_annotation['invokedBy'] = df_annotation['invokedBy'].str.replace(str_replace, "")
    df_invokeWf = df_annotation.loc[:, ['workflowName', 'invokedBy']].drop_duplicates()

    print(str(df_invokeWf), file=sys.stderr)

    #df_gefx = []
    df_gefx_source = []
    df_gefx_target = []

    counter = 0
    while counter < len(df_invokeWf):
        df_gefx_source.append(df_invokeWf.loc[counter][1])
        df_gefx_target.append(df_invokeWf.loc[counter][0])
        counter = counter + 1

    #combine source and target with no dupes
    df_node_list = df_gefx_source + df_gefx_target
    df_node_list = list(dict.fromkeys(df_node_list))

    # print(str(df_invokeWf.loc[counter][1]) + "-------" + str(counter) + "-------" + str(df_invokeWf.loc[counter][0]), file=sys.stderr)

    # translate workflow calls to a path graph
    #G = nx.from_pandas_edgelist(df_gefx, 'source', 'target')

    G = nx.DiGraph();
    G.add_nodes_from(df_node_list)
    print(str(G.nodes()), file=sys.stderr)

    counter = 0
    for i in range(0, len(df_invokeWf)):
        G.add_edge(df_gefx_source[i], df_gefx_target[i])
        print(str(df_gefx_source[i]) + "-------" + str(i) + "-------" + str(df_gefx_target[i]), file=sys.stderr)
        #counter = counter + 1

    print(str(G.edges()), file=sys.stderr)


    #ajax request so I dont have to store a file

    f = open('static/dist/project_structure_graph.gexf', "w+")
    f.truncate(0)
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')


    str_gexf = ""
    str_gexf = str_gexf + '<?xml version="1.0" encoding="UTF-8"?>\n'

    for line in nx.generate_gexf(G, encoding='utf-8', prettyprint=True, version='1.2draft'):
        #print(line, file=sys.stderr)
        f.write(line + '\n')
        str_gexf = str_gexf + line

    return str_gexf

