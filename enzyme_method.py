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
				print find_enzyme_digit(x)
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
		print res
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
			if float(tmp[1]) > 1.5:
				return "red"
			elif float(tmp[1]) >= 1.2:
				return "blue"
			elif float(tmp[1]) < 0.6:
				return "green"
			else:
				return "white"

def enzyme_foldchange_value(enzyme):
        f = open("data/gene_foldchange.csv","r")
        lines = f.readlines()
        for x in lines:
                if x.find(enzyme) != -1:
                        tmp = x.split(",")
			return tmp[1]

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
	#If okay return 0 , not okay 1
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
	if check_compound_2(compound) == 1:
		return 0
	return 1

def draw_neighbor(G,compound):
	tmp = nx.all_neighbors(G,compound)
	Gpart = nx.Graph()
	for x in tmp:
		Gpart.add_edge(x,compound,color=G.edge[x][compound]['color'])
	nx.draw(Gpart)
        plt.savefig("path_test.png")
        nx.draw_graphviz(Gpart)
        nx.write_dot(Gpart,'file_test.dot')

def check_compound(compound):
	pos = read_data("data/metabo_data_1126_pos_ave.csv")
        neg = read_data("data/metabo_data_1126_neg_ave.csv")

	for x in pos:
		tmp = compound.lower()
		print x
		if str(tmp).find(str(x[1].lower())) != -1:
			return 1

        for x in neg:
                tmp = compound.lower()
                if str(tmp).find(str(x[1].lower())) != -1:
                        return 1
	return 0

def check_compound_1(compound):
        pos = read_data("data/metabo_data_1126_pos_ave.csv")
        neg = read_data("data/metabo_data_1126_neg_ave.csv")

        for x in pos:
                tmp = compound.lower()
		print "opai"
		print x[2]
                if str(tmp) == str(x[1].lower()):
                        return 1

        for x in neg:
		tmp = compound.lower()
		if str(tmp) == str(x[1].lower()):
                        return 1
        return 0

def check_compound_2(compound):
        pos = read_data("data/metabo_data_1126_pos_ave.csv")
        neg = read_data("data/metabo_data_1126_neg_ave.csv")

        for x in pos:
                tmp = compound.lower()
                if str(tmp).find(str(x[1].lower())) != -1:
			if float(x[2]) != 0:
                        	return evaluate_foldchange(float(x[3])/float(x[2]))

        for x in neg:
                tmp = compound.lower()
                if str(tmp).find(str(x[1].lower())) != -1:
			if float(x[2]) != 0:
                        	return evaluate_foldchange(float(x[3])/float(x[2]))

def evaluate_foldchange(val):
	if val > 2.0 or val < 0.5:
		return 1
	return 0

def get_compound_foldchange(compound):
        pos = read_data("data/metabo_data_1126_pos_ave.csv")
        neg = read_data("data/metabo_data_1126_neg_ave.csv")

        for x in pos:
                tmp = compound.lower()
                if str(tmp).find(str(x[1].lower())) != -1:
			if float(x[2]) != 0:
                        	return float(x[3])/float(x[2])

     	for x in neg:
                tmp = compound.lower()
                if str(tmp).find(str(x[1].lower())) != -1:
			if float(x[2]) != 0:
                        	return float(x[3])/float(x[2])
        
	return -1
			

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

def write_edge(cx,cy):
        f2 = open("enzyme_edge_list.txt","a")
        f2.write(str(cx))
        f2.write("\t")
        f2.write(str(get_compound_foldchange(cx)))
        f2.write("\t")
        f2.write(str(cy))
        f2.write("\t")
        f2.write(str(get_compound_foldchange(cy)))
        f2.write("\n")
        f2.close()

if __name__ == "__main__":
	import itertools
	import matplotlib.pyplot as plt

	"""
	Workflow of this script:
	  1:Read gene_foldchange file
	  2:Find gene_related reaction(KEGG ACCESS)
	  3:Get compounds from reaction
	  4:Built network(Using NetworkX)
	  5:Mark up important edges
	"""

	G = nx.Graph()
	
	##Read gene data
	f = open("data/t_All_GSEA.csv","r")
	lines = f.readlines()
	f.close()

	f1 = open("enzyme_reaction_pair.txt","w")
	##related enzyme from gene
	for gene in lines:
		tmp = find_enzyme(extract_alphabet_from_gene(gene.strip()))
		f1.write(gene.strip("\n"))
		f1.write("\n")
		for x in tmp:
			reaction = find_related_equation(x)
			"""
			f1.write(x)
			f1.write("\t")
			for reac in reaction:
				if reac != "None":
					if check_reaction_compound(reac) == 0:
						f1.write(str(reac))
						f1.write("\t")
			"""
			if len(reaction) != 1:
				combi = list(itertools.combinations(range(len(reaction)), 2))
				for y in combi:
					if check_reaction_compound(reaction[y[0]]) == 0 and check_reaction_compound(reaction[y[1]]) == 0:
						f1.write(x.strip('\n'))
                        			f1.write("\t")
						f1.write(str(reaction[y[0]].strip('\n')))
						f1.write("\t")
						f1.write(str(reaction[y[1]].strip('\n')))
						G.add_edge(reaction[y[0]].strip('\n'),reaction[y[1]].strip('\n'),color=enzyme_foldchange(gene), weight=enzyme_foldchange_value(gene))
						f1.write("\n")
	f1.close()
	
	print G.edges()
	nx.write_gexf(G, "test_colors.gexf")
	#draw_neighbor(G,"D-glucose 6-phosphate")

	
	nx.draw(G)
	#plt.savefig("path.png")
	nx.draw_graphviz(G)
	nx.write_dot(G,'file.dot')
	
