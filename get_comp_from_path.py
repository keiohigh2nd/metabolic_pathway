# -*- coding: utf-8 -*-

import urllib2
import re

if __name__ == "__main__":

        path = "hsa05131"
	url = "http://rest.kegg.jp/get/%s/"%path
	htmldata = urllib2.urlopen(url)
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
