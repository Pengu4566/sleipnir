# project structure (invoking relationship)

import networkx as nx
import matplotlib.pyplot as plt


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
    plt.savefig('static/dist/project_structure.png')
    plt.close()

