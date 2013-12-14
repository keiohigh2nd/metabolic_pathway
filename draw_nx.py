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
	res = 0
        for x in data:
                tmp = x.split('\t')
		if name == tmp[1].strip("\n"):
			res =  tmp[0].strip("\n")
			print "found"
	return res
	
def search_compound(id):
	f = open("data/compound_id_converter.txt")
	data = f.readlines()
        res = 0
	for x in data:
		tmp = x.split('\t')
		if id == tmp[0].strip("\n"):
			res = tmp[1].strip("\n")
	return res

def read_data(filename):
	f = open(filename)
	data = f.readlines()
	f.close()

	res = []
	#If csv "," or "\t"
	for x in data:
		tmp = x.split(',')
		arr = []
		for y in tmp:
			if y:
				arr.append(y.strip('\r'))
		res.append(arr)

	return res
	
def Graph_info(G):
	print "Number of nodes is %d"%G.number_of_nodes()
        print "Number of edges is %d"%G.number_of_edges()	

def show_data(pos,neg,id):
	for x in pos:
		if id == x[0]:
			return x

	for x in neg:
		if id == x[0]:
			return x

def show_connections(G,pos,neg):
	for x in pos:
		try:
			tmp = nx.all_neighbors(G,x[0])
                        for y in tmp:
				print y

		except:
			print "Not Found"
	for y in neg:
		try:
			tmp = nx.all_neighbors(G,x[0])
                        for y in tmp:
				print y
		except:
			print "Not Found"
			
	

if __name__ == "__main__":

	#Read Compound
	pos = read_data("data/metabo_data_1126_pos_ave.csv")
        neg = read_data("data/metabo_data_1126_neg_ave.csv")


	#Test
	#id = search_id("Pelargonate")
	#print "This is the id = %s"%id



	#Draw Network
	f = open('data/node_neo.txt')
	lines2 = f.readlines()
	f.close()

	G = nx.Graph()

	for line in lines2:
   		tmp  = line.split('\t')
   		G.add_edge(tmp[0].strip('\n'),tmp[1].strip('\n'))
	

	#Write Result
	f1 = open('result.txt','w')

	for x in pos:
		try:
			for t in x:
				f1.write(t)
				f1.write('\t')
			print x
			tmp = nx.all_neighbors(G,x[0])
			for x1 in tmp:
				tmp_data = show_data(pos,neg,x1)
				print tmp_data
				for z in tmp_data:
					f1.write(z)
					f1.write('\t')
			f1.write('\n')
		except:
			print "not found"

	for y in neg:
		try:
			for t in y:
                                f1.write(t)
                                f1.write('\t')
                        tmp = nx.all_neighbors(G,y[0])
                        for y1 in tmp:
                                tmp_data = show_data(pos,neg,y1)
                                for z in tmp_data:
                                        f1.write(z)
                                        f1.write('\t')
			f1.write('\n')
		except:
			print "not found"


	f1.close()

	print "koko"	
	to = nx.all_neighbors(G,"C01060")
	for k in to:
		print k	
