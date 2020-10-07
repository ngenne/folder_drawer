# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:06:04 2020

@author: NGENNE
"""

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

    if not os.path.isdir(path):
        print('The path specified does not exist')
        sys.exit()
        
    df = folderstats.folderstats(path, ignore_hidden=True, absolute_paths=False)
    
    df_sorted = df[df['folder'] == True].sort_values(by='id').set_index('id')
    df_sorted = pd.DataFrame(df_sorted)
    
    nodes_names = df_sorted['name']
    nodes_names = pd.DataFrame(nodes_names)
    
    G = nx.Graph(directed=True)
    
    for i, row in df_sorted.iterrows():
        if row.parent:
            G.add_edge(i, row.parent)
    
    g_nodes = list(G.nodes)
    nodes_names = nodes_names.loc[g_nodes]
    
    for node in G.nodes():
        G.nodes[node]['label'] = nodes_names['name'][node]
    
    nx.write_graphml(G, 'map_{}.graphml'.format(datetime.datetime.today().strftime("%Y-%m-%d--%H%M%S")))

    print('Mapping complete')

if __name__ == '__main__':
    folder_drawer(sys.argv[1])
