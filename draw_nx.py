#!/usr/bin/python
# coding: UTF-8

import matplotlib
matplotlib.use('Agg')

try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx
import re
 
f = open('node_neo.txt')
lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
f.close()
# lines2: リスト。要素は1行の文字列データ

G = nx.Graph()

for line in lines2:
   tmp  = line.split('\t')
   G.add_edge(tmp[0],tmp[1])


nx.draw(G)
plt.savefig("path.png")
plt.show()

 
