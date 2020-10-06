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

def scan2map(path):
    path = args.Path

    if not os.path.isdir(path):
        print('The path specified does not exist')
        sys.exit()
        
    # Recupere les stats des dossiers parcourus
    df = folderstats.folderstats(path, ignore_hidden=True, absolute_paths=False)
    
    # Retenu des dossiers seulement et tri sur la valeur 'id'
    df_sorted = df[df['folder'] == True].sort_values(by='id').set_index('id')
    df_sorted = pd.DataFrame(df_sorted)
    
    # Recuperation des noms des dossiers pour mettre a jour les noeuds du reseau
    nodes_names = df_sorted['name']
    nodes_names = pd.DataFrame(nodes_names)
    
    # Creation du graph
    G = nx.Graph(directed=True)
    
    # Creation des aretes du reseau a partir des variables 'parent' et 'id' de df_sorted
    for i, row in df_sorted.iterrows():
        if row.parent:
            G.add_edge(i, row.parent)
    
    # Recup de l'index des noeuds et reindexation du dataframe nodes_names avec g_nodes
    g_nodes = list(G.nodes)
    nodes_names = nodes_names.loc[g_nodes]
    
    # Ajout des proprietes "label" pour chaque noeud afin de faciliter le mapping des labels dans yEd
    for node in G.nodes():
        G.nodes[node]['label'] = nodes_names['name'][node]
    
    # Sauvegarde du graph en format XML
    nx.write_graphml(G, 'map_{}.graphml'.format(datetime.datetime.today().strftime("%Y-%m-%d--%H%M%S")))

    print('Mapping complete')

if __name__ == '__main__':
    scan2map(sys.argv[1])


# TESTS
# Afficher les carateristiques du reseau
# print(nx.info(G))
# plt.savefig('network_{}.svg'.format(datetime.datetime.today().strftime("%Y-%m-%d--%H_%M_%S")))