# -*- coding: utf-8 -*-

import xlrd
import xlwt
import string
import math

def average(a):
	sum = 0
	for v in a:
		sum += v
	return float(sum)/len(a)

def disp(a,ave):
	sum = 0
	for v in a:
		sum += math.pow(v-ave, 2)
	return float(sum) / (len(a) - 1)

def fold_change(gene,comp):
	i = 0
	gray, cont = 0
	for x in comp:
		if i > 4:
			gray += x
		else:
			cont += x
	return gene - (float(gray)/4-float(cont)/4)

def get_average(res):
	i = 0
	gray = 0
	normal = 0
	ko = []
	for x in res:
		if i < 5:
			normal += float(x)
		else:
			gray += float(x)
		i += 1
	ko.append(float(normal)/5)
	ko.append(float(gray)/5)
	return ko

if __name__ == "__main__":
	meta_book = xlrd.open_workbook('data/neg_x_data.xlsx')
	meta_sheet = meta_book.sheet_by_index(0)

	f = open('text.txt', 'w')

	for col in range(meta_sheet.nrows):
		res = []
		tmp = []
		for row in range(meta_sheet.ncols):
			res.append(meta_sheet.cell(col,row).value)
		tmp = get_average(res)
		for x in tmp:
			f.write(str(x))
			f.write('\t')
		f.write('\n')	
		
	
	f.close()

