# project structure (invoking relationship)

import networkx as nx
import os
import sys
import pandas as pd


def generate_gexf(df_annotation, main_location):
    str_replace = main_location + "/"
    df_annotation['workflowName'] = df_annotation['workflowName'].str.replace(str_replace, "")
    df_annotation['invokedBy'] = df_annotation['invokedBy'].str.replace(str_replace, "")
    df_invokeWf = df_annotation.loc[:, ['workflowName', 'invokedBy']].drop_duplicates()
    #combine source and target with no dupes
    df_node_list = list(pd.concat([df_invokeWf.loc[:, 'invokedBy'], df_invokeWf.loc[:, 'workflowName']], ignore_index= True).drop_duplicates())
    # print(str(df_invokeWf.loc[counter][1]) + "-------" + str(counter) + "-------" + str(df_invokeWf.loc[counter][0]), file=sys.stderr)
    # translate workflow calls to a path graph
    G = nx.DiGraph();
    G.add_nodes_from(df_node_list)
    # print(str(G.nodes()), file=sys.stderr)
    for index, row in df_invokeWf.iterrows():
        G.add_edge(row['invokedBy'], row['workflowName'])

    #ajax request so I dont have to store a file
    f = open('static/dist/project_structure_graph.gexf', "w+")
    f.truncate(0)
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    str_gexf = ""
    str_gexf = str_gexf + '<?xml version="1.0" encoding="UTF-8"?>\n'
    for line in nx.generate_gexf(G, encoding='utf-8', prettyprint=True, version='1.2draft'):
        f.write(line + '\n')
        str_gexf = str_gexf + line
    f.close()
    return str_gexf

