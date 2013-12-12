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
 
def make_dic():
        f = open("data/compound_id_converter.txt")
        data = f.readlines()

        dict = {}
        for x in data:
                tmp = x.split('\t')
                dict.update({tmp[1].strip("\n"):tmp[0].strip("\n")})

        return dict

def search_id(name):
        f = open("data/compound_id_converter.txt")
        data = f.readlines()

        for x in data:
                tmp = x.split('\t')
		if name == tmp[1].strip("\n"):
			return tmp[0].strip("\n")

	return 0

def read_data(filename):
	f = open(filename)
	data = f.readlines()
	f.close()

	res = []
	for x in data:
		tmp = x.split('\t')
		arr = []
		for y in tmp:
			if y:
				arr.append(y.strip('\n'))
		res.append(arr)

	return res
	
		
	

if __name__ == "__main__":

	#Read Compound
	pos = read_data("data/gene_compound_1126_pos_nonND.txt")
        neg = read_data("data/gene_compound_1126_neg_nonND.txt")


	id = search_id("Pelargonate")
	print id
        #dict = make_dic()


	for x in pos:
		id = search_id(x[0])

        for x in neg:
		id = search_id(x[0])

	#Draw Network
	f = open('data/node_neo.txt')
	lines2 = f.readlines()
	f.close()

	G = nx.Graph()

	for line in lines2:
   		tmp  = line.split('\t')
   		G.add_edge(tmp[0].strip('\n'),tmp[1].strip('\n'))
	
	print G.nodes()
	tmp = nx.all_neighbors(G,"C04807")

	for x in tmp:
		print x
