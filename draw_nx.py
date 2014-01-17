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
import get_compounds_from_gene2 

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
			
	
def read_gene(compound_id):
	f = open("data/gene_compound_all.txt")
	lines = f.readlines()
	f.close()

	for x in lines:
		tmp = x.split("\t")
		if compound_id == tmp[2]:
			print "Find GENE"
			return tmp[0]

def gene_foldchange(gene):
	f = open("data/gene_foldchange.csv")
	lines = f.readlines()
	f.close()

	for x in lines:
		tmp = x.split(",")
		if tmp[0].upper() == gene:
			return tmp[1]

				
def Draw_Graph(file_name):
	f = open(file_name)
        lines2 = f.readlines()
        f.close()

        G = nx.Graph()

        for line in lines2:
                tmp  = line.split('\t')
                G.add_edge(tmp[0].strip('\n'),tmp[1].strip('\n'))

	return G

def Find_Neighbors(G, pos, neg):
	#Write Result
        f1 = open('result.txt','w')

        for x in pos:
                try:
                        tmp = nx.all_neighbors(G,x[0])
                        for t in x:
                                f1.write(t.strip('\r\n'))
                                f1.write('\t')
			#All neighbors
                        for x1 in tmp:
                                tmp_data = show_data(pos,neg,x1)
                                for z in tmp_data:
                                        f1.write(z.strip('\r\n'))
                                        f1.write('\t')
				#Neighbors of query compound try to find related gene
				tmp_gene = read_gene(tmp_data[0])
				if tmp_gene:
					f1.write(tmp_gene.strip('\r\n'))
					f1.write('\t')
					f1.write(gene_foldchange(tmp_gene).strip('\n'))
					f1.write('\t')
			res_gene = read_gene(x[0])
			#Query Compound Related Gene
			if res_gene:
				f1.write(res_gene.strip('\r\n')) 
				f1.write("\t")
				f1.write(gene_foldchange(res_gene).strip('\n'))
                        f1.write('\n')
                except:
                        #print "not found"
			#f1.write(x[1])
                        f1.write('\n')

        for y in neg:
                try:
                        tmp = nx.all_neighbors(G,y[0])
                        for t in y:
                                f1.write(t.strip('\r\n'))
                                f1.write('\t')
                        for y1 in tmp:
                                tmp_data = show_data(pos,neg,y1)
                                for z in tmp_data:
                                        f1.write(z.strip('\r\n'))
                                        f1.write('\t')
				#Neighbors of query compound try to find related gene
				tmp_gene = read_gene(tmp_data[0])
                                if tmp_gene:
                                        f1.write(tmp_gene.strip('\n'))
                                        f1.write('\t')
					f1.write(gene_foldchange(tmp_gene).strip('\n'))
					f1.write('\t')
                        res_gene = read_gene(y[0])
                        #Query Compound Related Gene
                        if res_gene:
                                f1.write(res_gene.strip('\r\n'))
				f1.write('\t')
				f1.write(gene_foldchange(res_gene).strip('\n'))
                        f1.write('\n')
                except:
                        #print "not found"
			#f1.write(y[1])
                        f1.write('\n')
	f1.close()

def Find_Neighbors2(pos, neg):
        #Write Result
        f1 = open('result.txt','w')

        for x in pos:
                try:
                        tmp = get_neighbor2(x[0])
			print tmp
                        for t in x:
				print "WRITE"
                                f1.write(t.strip('\r\n'))
                                f1.write('\t')
                        #All neighbors
                        for x1 in tmp:
                                tmp_data = show_data(pos,neg,x1)
                                for z in tmp_data:
                                        f1.write(z.strip('\r\n'))
                                        f1.write('\t')
                                #Neighbors of query compound try to find related gene
                                tmp_gene = read_gene(tmp_data[0])
                                if tmp_gene:
                                        f1.write(tmp_gene.strip('\r\n'))
                                        f1.write('\t')
                                        f1.write(gene_foldchange(tmp_gene).strip('\n'))
                                        f1.write('\t')
                        res_gene = read_gene(x[0])
                        #Query Compound Related Gene
                        if res_gene:
                                f1.write(res_gene.strip('\r\n'))
                                f1.write("\t")
                                f1.write(gene_foldchange(res_gene).strip('\n'))
                        f1.write('\n')
                except:
                        #print "not found"
                        #f1.write(x[1])
                        f1.write('\n')

        for y in neg:
                try:
                        tmp = get_neighbor2(y[0])
                        for t in y:
				print "write"
                                f1.write(t.strip('\r\n'))
                                f1.write('\t')
                        for y1 in tmp:
                                tmp_data = show_data(pos,neg,y1)
                                for z in tmp_data:
                                        f1.write(z.strip('\r\n'))
                                        f1.write('\t')
                                #Neighbors of query compound try to find related gene
                                tmp_gene = read_gene(tmp_data[0])
                                if tmp_gene:
                                        f1.write(tmp_gene.strip('\n'))
                                        f1.write('\t')
                                        f1.write(gene_foldchange(tmp_gene).strip('\n'))
                                        f1.write('\t')
                        res_gene = read_gene(y[0])
                        #Query Compound Related Gene
                        if res_gene:
                                f1.write(res_gene.strip('\r\n'))
                                f1.write('\t')
                                f1.write(gene_foldchange(res_gene).strip('\n'))
                        f1.write('\n')
                except:
                        #print "not found"
                        #f1.write(y[1])
                        f1.write('\n')
        f1.close()




def get_neighbor2(id):
	f = open("data/hsa_list.txt")
	line = f.readlines()
	res = []
	for x in line:
		tmp = get_compounds_from_gene2.get_compound(x[5:13])
		for y in tmp:
			#If id is in the passway
			if id == y:
				res.append(tmp)
				break
	return res

if __name__ == "__main__":

	#Read Compound
	pos = read_data("data/metabo_data_1126_pos_ave.csv")
        neg = read_data("data/metabo_data_1126_neg_ave.csv")
	
	#G = Draw_Graph("data/node_neo.txt")

	#Test
	"""
	tmp = nx.all_neighbors(G,"C00311")
	for x in tmp:
		print x

        tmp = get_neighbor2("C00311")
        print tmp
	"""

	Find_Neighbors2(pos,neg)

