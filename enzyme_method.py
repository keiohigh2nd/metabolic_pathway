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
			if tmp[1] <= 0.8:
				return "blue"
			return "green"

def extract_alphabet_from_gene(gene):
	for i in xrange(len(gene)):
		if gene[i].isdigit() == True:
			return gene[0:i]

if __name__ == "__main__":
	print extract_alphabet_from_gene("Pdp2")

	G = nx.Graph()
	f = open("data/gene_foldchange.csv","r")
	lines = f.readlines()
	f.close()

	f1 = open("enzyme_reaction_pair.txt","w")
	##related enzyme from gene
	for gene in lines:
		tmp = find_enzyme(extract_alphabet_from_gene(gene.strip()))
		f1.write(gene.strip())
		f1.write("\t")
		for x in tmp:
			print x
			reaction = find_related_reaction(x)
			for reac in reaction:
				rpair = get_reaction_compound(reac)
				if rpair != "None":	
					f1.write(rpair[0])
					f1.write("\t")
					f1.write(str(rpair[1]))
					f1.write("\n")
					G.add_edge(rpair[0].strip('\n'),rpair[1].strip('\n'),color=enzyme_foldchange(gene))

	print G.edges()
