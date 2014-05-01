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


def check_compound(compound):
        pos = read_data("data/metabo_data_1126_pos_ave.csv")
        neg = read_data("data/metabo_data_1126_neg_ave.csv")

	if compound.find("H2O") != -1:
                return 0
        if compound.find("CO2") != -1:
                return 0
        if compound.find("NH3") != -1:
                return 0
        if compound.find("H") != -1:
                return 0
        if not compound:
                return 0


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
        if float(val) > float(2.0)or float(val) < float(0.3):
                return 1
        return 0

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

def array_line(line):
    tmp = line.split("\t")
    del tmp[0]
    del tmp[-1]
    try:
    	del tmp[-1]
	return tmp
    except:
	return tmp
		

if __name__ == "__main__":
	import itertools

	f = open("enzyme_reaction_pair.txt")
	lines = f.readlines()
	f.close()

	f1 = open("arrayed_enzyme_reaction.txt","w")

	for line in lines:
		if line.find("ec:") != 0:
			tmp = line.split("\t")
			f1.write(tmp[0])
			f1.write("\t")
			f1.write(tmp[1])
			f1.write("\n")
		else:
			line = line.strip("\n")	
			tmp = array_line(line)
			combi = list(itertools.combinations(range(len(tmp)), 2))
                	for x in combi:
				if check_compound(tmp[x[0]].strip("\n")) == 1 and check_compound(tmp[x[1]].strip("\n")) == 1:
					print tmp[x[0]].strip("\n")
					f1.write(tmp[x[0]].strip("\n"))
					f1.write("\t")
					f1.write(tmp[x[1]].strip("\n"))
					f1.write("\n")

	f1.close()
