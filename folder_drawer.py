# -*- coding: utf-8 -*-

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
        path = (r'\\?\UNC' + path[1:])
    else:
        pass

    if not os.path.isdir(path):
        print('The path specified does not exist')
        sys.exit()
        
    df = folderstats.folderstats(path, ignore_hidden=True, absolute_paths=False)
    
    df_sorted = df[df['folder'] == True].sort_values(by='id').set_index('id')
    df_sorted = pd.DataFrame(df_sorted)
    
    df_sorted['empty'] = ''
    
    for each in df_sorted['path']:
        if not os.listdir(each):
            df_sorted['empty'][df_sorted['path'] == each] = True
        else:
            df_sorted['empty'][df_sorted['path'] == each] = False
    
    nodes_names = df_sorted['name']
    nodes_names = pd.DataFrame(nodes_names)
    
    nodes_empty = df_sorted['empty']
    nodes_empty = pd.DataFrame(nodes_empty)
    
    G = nx.Graph(directed=True)
    
    for i, row in df_sorted.iterrows():
        if row.parent:
            G.add_edge(i, row.parent)
    
    g_nodes = list(G.nodes)
    nodes_names = nodes_names.loc[g_nodes]
    nodes_empty = nodes_empty.loc[g_nodes]
    
    for node in G.nodes():
        G.nodes[node]['label'] = nodes_names['name'][node]
        G.nodes[node]['empty'] = nodes_empty['empty'][node]
    
    nx.write_graphml(G, 'map_{}.graphml'.format(datetime.datetime.today().strftime("%Y-%m-%d--%H%M%S")))

    print('Mapping complete')

if __name__ == '__main__':
    folder_drawer(sys.argv[1])
