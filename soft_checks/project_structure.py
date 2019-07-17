# project structure (invoking relationship)

import networkx as nx
import os
import sys
import pandas as pd


def generate_gexf(df_annotation, fileLocationStr):
    df_annotation_dup = df_annotation.copy()
    df_annotation_dup['workflowName'] = df_annotation_dup['workflowName'].str.replace(fileLocationStr, "")
    df_annotation_dup['invokedBy'] = df_annotation_dup['invokedBy'].str.replace(fileLocationStr, "")
    df_invokeWf = df_annotation_dup.loc[:, ['workflowName', 'invokedBy']].drop_duplicates()
    #combine source and target with no dupes
    df_node_list = list(pd.concat([df_invokeWf.loc[:, 'invokedBy'], df_invokeWf.loc[:, 'workflowName']], ignore_index= True).drop_duplicates())
    # translate workflow calls to a path graph
    G = nx.DiGraph();
    G.add_nodes_from(df_node_list)

    for index, row in df_invokeWf.iterrows():
        G.add_edge(row['invokedBy'], row['workflowName'])

    #ajax request
    str_gexf = '<?xml version="1.0" encoding="UTF-8"?>\n' + "".join(nx.generate_gexf(G, encoding='utf-8', prettyprint=True, version='1.2draft'))

    return str_gexf

