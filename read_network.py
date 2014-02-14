# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx
import get_compounds_from_gene2

import urllib2
import re
import xlrd
import os

def find_enzyme_digit(line):
	for i in xrange(len(line)):
		if line[i] == "\t":
			return line[0:i]

def find_enzyme(enzyme):
        url = "http://rest.kegg.jp/find/enzyme/%s/"%enzyme
        res = []

        try:
                htmldata = urllib2.urlopen(url)
        except:
                res.append('')
                return res

        else:
                tmp = unicode(htmldata.read(),"utf-8")
                htmldata.close()
		lines =  tmp.split("\n")
		f = open("gene_not_found.txt","w")
		if lines[0] == "":
			f.write(lines[0])
			f.write("\n")
			f.close()
		for x in lines:
			if x != "":
				#print find_enzyme_digit(x)
				res.append(find_enzyme_digit(x))
		return res

def find_related_reaction(enzyme):
        url = "http://rest.kegg.jp/get/%s/"%enzyme
        res = []

        try:
                htmldata = urllib2.urlopen(url)
        except:
                res.append('')
                return res

        else:
                tmp = unicode(htmldata.read(),"utf-8")
                htmldata.close()
                lines = tmp.split("\n")
		for x in lines:
			if x.find("ALL_REAC") != -1:
				tmp = x.split("    ")
				reac = tmp[1].split(" ")
				for x in reac:
					res.append(x)
		return res

def find_related_equation(enzyme):
        url = "http://rest.kegg.jp/get/%s/"%enzyme
        res = []

        try:
                htmldata = urllib2.urlopen(url)
        except:
                res.append('')
                return res

        else:
                tmp = unicode(htmldata.read(),"utf-8")
                htmldata.close()
                lines = tmp.split("\n")
                for x in lines:
                        if x.find("REACTION") != -1:
                                tmp = x.split("    ")
                                reac = tmp[1].split("=")
                                for x in reac:
                                        rea = x.split("+")
					for y in rea:
						if y.find("[RN") != -1:
							tmp = y.split(" ")
							tmp1 = y.strip(tmp[-1])
							res.append(tmp1.strip())
						else:
							res.append(y.strip())
                return res

def get_reaction_compound(reaction):
        url = "http://rest.kegg.jp/get/%s"%reaction.strip()
	res = []
        try:
                htmldata = urllib2.urlopen(url)
        except:
                print "NOT FOUND"
		return 1

        else:
                tmp = unicode(htmldata.read(),"utf-8")
                htmldata.close()
                start = tmp.find("RPAIR")
		end = tmp.find("ENZYME")
                lines = tmp[start+6:end].split("\n")
		for x in lines:
			tmp = x.find("main")
			if tmp != -1:
				res.extend(x[tmp-14:tmp-1].split("_"))
				return res

def enzyme_foldchange(enzyme):
	f = open("data/gene_foldchange.csv","r")
	lines = f.readlines()
	for x in lines:
		if x.find(enzyme) != -1:
			tmp = x.split(",")
			if tmp[1] >= 1.5:
				return "red"
			if tmp[1] >= 1.2:
				return "blue"
			if tmp[1] <= 0.6:
				return "green"
			return "black"

def extract_alphabet_from_gene(gene):
	for i in xrange(len(gene)):
		if gene[i].isdigit() == True:
			return gene[0:i]

def combination_reaction(G,reaction,gene):
	tmp = list(itertools.combinations(range(len(reaction)), 2))
	for x in tmp:
		G.add_edge(reaction[x[0]].strip('\n'),reaction[x[1]].strip('\n'),color=enzyme_foldchange(gene))
	return G

def check_reaction_compound(compound):
	if compound.find("H2O") != -1:
		return 1
	if compound.find("CO2") != -1:
		return 1
	if compound.find("NH3") != -1:
		return 1
	if compound.find("H") != -1:
		return 1
	if not compound:
		return 1
	return 0

def draw_neighbor(G,compound):
	tmp = G.neighbors(str(compound))
	Gpart = nx.Graph()
	print tmp
	for x in tmp:
		#print x
		print G.edge[x][compound]['weight']
		Gpart.add_edge(x,compound,color=G.edge[x][compound]['color'],weight=G.edge[x][compound]['weight'])
	nx.draw(Gpart)
	name = "path_%s.png"%str(compound)
        plt.savefig(name)
        
	nx.draw_graphviz(Gpart)
	name1 = "file_%s.dot"%str(compound)
        nx.write_dot(Gpart,name1)

def search_biggest_node(G,node):
	edges = G.edges(node)
	if len(edges) <= 2:
                print "This is the terminal"
                return 0
	max_edge = 0
	max_i = 0
	i = 0
	for x in edges:
                if max_edge < G.edge[node][x[1]]['weight']:
                        max_edge = G.edge[node][x[1]]['weight']
                        max_i = i
		i += 1
	#print edges[max_i][1]
	# Edges = [self, toward]
	return edges[max_i][1]

def trace_node(G,first_node):
	edges = G.edges(first_node)
	if len(edges) <= 2:
		print "This is the terminal"
		return 0
	
	max_edge = 0
	max_edge2 = 0
	max_edge3 = 0
	max_i = 0
	max_i2 = 0
        max_i3 = 0
	i = 0
	for x in edges:
		if max_edge < G.edge[first_node][x[1]]['weight']:
			max_edge = G.edge[first_node][x[1]]['weight']
			max_i = i
		else:
			if max_edge2 < G.edge[first_node][x[1]]['weight']:
				max_edge2 = G.edge[first_node][x[1]]['weight']
                               	max_i2 = i
			else:
				if max_edge3 < G.edge[first_node][x[1]]['weight']:
                                	max_edge3 = G.edge[first_node][x[1]]['weight']
                                	max_i3 = i

		i += 1
	#print G.edge[first_node][edges[max_i][1]]['color']
	print first_node,edges[max_i][1],edges[max_i2][1], len(edges)
	#If the biggest edge is original edges
        return trace_node_rec(G,edges[max_i][1],first_node)

def trace_node_rec(G,first_node, second_node):
        edges = G.edges(first_node)
        if len(edges) <= 2:
                print "This is the terminal"
                return 0

        max_edge = 0
        max_edge2 = 0
        max_edge3 = 0
        max_i = 0
        max_i2 = 0
        max_i3 = 0
        i = 0
        for x in edges:
                if max_edge < G.edge[first_node][x[1]]['weight']:
                        max_edge = G.edge[first_node][x[1]]['weight']
                        max_i = i
                else:
                        if max_edge2 < G.edge[first_node][x[1]]['weight']:
                                max_edge2 = G.edge[first_node][x[1]]['weight']
                                max_i2 = i
                        else:
                                if max_edge3 < G.edge[first_node][x[1]]['weight']:
                                        max_edge3 = G.edge[first_node][x[1]]['weight']
                                        max_i3 = i

                i += 1
        #print G.edge[first_node][edges[max_i][1]]['color']
        print first_node,edges[max_i][1],edges[max_i2][1], len(edges)
        #If the biggest edge is original edges
        if str(edges[max_i][1]) == str(second_node):
		print search_biggest_node(G,second_node)
                if str(edges[max_i2][1]) != str(search_biggest_node(G,second_node)):
                        print "second"
                        return trace_node_rec(G,edges[max_i2][1],first_node)
                else:
                        if len(edges) > 3:
                                print "third"
                                return trade_node_rec(G,edges[max_i3][1],first_node)
	else:
                print "first"
                return trace_node_rec(G,edges[max_i][1],first_node)

      


	
if __name__ == "__main__":
	import itertools
	import matplotlib.pyplot as plt
	
	G = nx.read_gexf("test_colors.gexf")
	#draw_neighbor(G,"S-adenosyl-L-methionine")

	#search_biggest_node(G,"ADP")
	trace_node(G,"ADP")
		
	"""	
	nx.draw(G)
	#plt.savefig("path.png")
	nx.draw_graphviz(G)
	nx.write_dot(G,'file.dot')
	"""
