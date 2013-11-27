# -*- coding: utf-8 -*-

import urllib2
import re
import xlrd
import xlwt

def read_path2(file_name):
	f = open(file_name)
	lines = f.readlines()
	f.close()
	
	res = []
	p = re.compile(r'^[a-z]+')

	for x in lines:
		gene = x.split('\t')
		tmp = x.strip(gene[0])
		tmp1 = tmp.strip('\t')
		tmp2 = tmp1.strip('\n')
		arr = tmp2.split(',')
		print arr
		for y in arr:
			if p.match(tmp2,0) != None:
				res.append((gene[0], y.strip('\n')))
	return res

def read_path(file_name):
        f = open(file_name)
        lines = f.readlines()
        f.close()

        res = []
        p = re.compile(r'^[a-z]+')

        for x in lines:
                arr = x.split(',')
                for y in arr:
                        if p.match(x,0) != None:
                                res.append(y.strip('\n'))
        return res

def get_compound(path_name):
        url = "http://rest.kegg.jp/get/%s/"%path_name
	res = []

        try:
		htmldata = urllib2.urlopen(url)
	except:
		res.append('')
		return res
	
	else:	
        	tmp = unicode(htmldata.read(),"utf-8")
        	htmldata.close()

        	start = tmp.find("COMPOUND")
        	end = tmp.find("REFERENCE")

        	fin =  tmp[start+8:end]
        	fin1  = fin.split(' ')

        	p = re.compile(r'\d+')
        	for x in fin1:
                	if p.match(x,1) != None:
				if re.match(r'C',x) != None:
					res.append(x)

		return res

def get_fold_change(arr):
	i = 0
	cont = 0
	res = []
	for x in arr:
		if i < 5:
			cont += x
		else:
			tmp = float(cont)/4
			res.append(tmp)
			i = 0
	return res

def get_average(arr):
	i = 0
	cont = 0
	res = []
	for x in arr:
		if i < 4:
			cont += x
		else:
			tmp = float(cont)/4
			res.append(tmp)
			i = 0

	return res

def read_compound(compound):
	meta_book = xlrd.open_workbook('metabo_data_1126_neg.xlsx')
        meta_sheet = meta_book.sheet_by_index(0)

	res = []
	for col in range(meta_sheet.nrows):
		if meta_sheet.cell(col,0).value == compound:
			for row in range(meta_sheet.ncols):
				res.append(meta_sheet.cell(col,row).value)
				
	return res
	


if __name__ == "__main__":

	#get compound from hsa
	f1 = open("gene_compound.txt", "w")

	#result txt
	f2 = open("final_result.txt", "w")

	#Known Pathways
	#reading pathway
	path_list = ("kegg_path2.txt")
	res = read_path2(path_list)

	print res	
	ic = 0
	for path_name in res:
		ic += 1
		print ic
		if path_name[1].find('hs') != -1:
			#get compoounds from one pathway
			tmp = get_compound(path_name[1])
			for x in tmp:
				f1.write(path_name[0])
                                f1.write("\t")
	                        f1.write(path_name[1])
                                f1.write("\t")
				#finding compounds from metabolome data
				tmp1 = read_compound(x)
				
				#Can' find compound from experiments
				if tmp1 != None:
					for y in tmp1:
						f1.write(str(y))
						f1.write("\t")
				else:
					f1.write(x)
				f1.write("\n")
				
	f1.close()
	f2.close()
	#get the same compound from metabolome data


