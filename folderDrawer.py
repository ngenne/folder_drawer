# -*- coding: utf-8 -*-
'''
« Copyright 2020 Niels Genne »
'''

import folderstats
import networkx as nx
import pandas as pd
import datetime
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('Path', help='List and draw recursively the content of folders')
args = parser.parse_args()

def folder_drawer(path):
    path = args.Path
    if path.startswith(r'\\'):
        path = (r'\\?\UNC' + path[1:]) # if UNC path this prefix is added
    else:
        pass # else it is a local path, so keep it as initial
    
    # Check if the path specified exists
    if not os.path.isdir(path):
        print('The path specified does not exist')
        sys.exit()
    
    # Retrieves the statistics of the browsed files
    df = folderstats.folderstats(path, ignore_hidden=True, absolute_paths=False)
    # Holds folders only and sort on the value 'id'.
    df_sorted = df[df['folder'] == True].sort_values(by='id').set_index('id')
    df_sorted = pd.DataFrame(df_sorted)
    
    # Variable 'too_old' added to display if last access time is older than 1 year (True) or not (False)
    df_sorted['too_old'] = ''
    df_sorted['atime'] = pd.to_datetime(df_sorted['atime'])
    
    for each in df_sorted['atime']:
        if datetime.datetime.today() - each > datetime.timedelta(days=365):
            df_sorted.loc[df_sorted['atime'] == each, ['too_old']] = True # More than 1 year
        else:
            df_sorted.loc[df_sorted['atime'] == each, ['too_old']] = False # Less than 1 year
    
    # Variable 'empty' added to display if folder is empty (True) or not (False)
    df_sorted['empty'] = ''
    
    for each in df_sorted['path']:
        if not os.listdir(each):
            df_sorted.loc[df_sorted['path'] == each, ['empty']] = True
        else:
            df_sorted.loc[df_sorted['path'] == each, ['empty']] = False
    
    # Folder name retrieval to update network nodes and colors if folder is empty/full
    # label (yEd)
    nodes_names = df_sorted['name']
    nodes_names = pd.DataFrame(nodes_names)
    # empty (yEd)
    nodes_empty = df_sorted['empty']
    nodes_empty = pd.DataFrame(nodes_empty)
    # too_old (yEd)
    nodes_too_old = df_sorted['too_old']
    nodes_too_old = pd.DataFrame(nodes_too_old)
    
    # NetworkX Graph creation
    G = nx.Graph(directed=True)
    
    # Creation of network edges from the 'parent' and 'id' variables of df_sorted
    for i, row in df_sorted.iterrows():
        if row.parent:
            G.add_edge(i, row.parent)
    
    # Recovery of the node index and reindexing of dataframes with "g_nodes"
    g_nodes = list(G.nodes)
    nodes_names = nodes_names.loc[g_nodes]
    nodes_empty = nodes_empty.loc[g_nodes]
    nodes_too_old = nodes_too_old.loc[g_nodes]
    
    # Adding 'label', 'empty' and 'too_old' properties for each node to ease properties mapping in yEd
    for node in G.nodes():
        G.nodes[node]['label'] = nodes_names['name'][node]
        G.nodes[node]['empty'] = nodes_empty['empty'][node]
        G.nodes[node]['too_old'] = nodes_too_old['too_old'][node]
    
    # Saving the graph in XML format
    nx.write_graphml(G, 'map_{}.graphml'.format(datetime.datetime.today().strftime("%Y-%m-%d--%H%M%S")))

    print('Mapping complete')

if __name__ == '__main__':
    folder_drawer(sys.argv[1])
