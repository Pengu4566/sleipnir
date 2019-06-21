# project structure (invoking relationship)

import networkx as nx
import matplotlib.pyplot as plt
from os import path
import time
from random import randint


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

    picStore = "/".join(main_location.split("/")[:-3]) + "/static/dist/chart/project_structure"\
               + str(time.time()).replace(".", "") + str(randint(1, 99999999999)) + ".png"
    picExists = path.isfile(picStore)
    while picExists:
        picStore = "/".join(main_location.split("/")[:-3]) + "/static/dist/chart/project_structure" \
                   + str(time.time()).replace(".", "") + str(randint(1, 99999999999)) + ".png"
        picExists = path.isfile(picStore)

    plt.savefig(picStore)
    plt.close()
    return picStore


