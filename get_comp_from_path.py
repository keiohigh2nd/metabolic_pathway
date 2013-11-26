# -*- coding: utf-8 -*-

import urllib2
import re

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
				print y
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
                        	print x
				res.append(x)

		return res


if __name__ == "__main__":

	f1 = open("gene_compound.txt","w")

	path_list = ("kegg_path.txt")
	res = read_path(path_list)

	for path_name in res:
		if path_name.find('hs') != -1:
			tmp = get_compound(path_name)
			for x in tmp:
				print x
				f1.write(x)

	f1.close()

