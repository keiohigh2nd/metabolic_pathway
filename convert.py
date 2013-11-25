#!/usr/bin/python
# coding: UTF-8
import re
 
f = open('node.txt')
lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
f.close()
# lines2: リスト。要素は1行の文字列データ

f1 = open("node_neo.txt", 'w')

i = 0
j = 0
for line in lines2:
    #From Reaction to COMPOUND
    tmp1 = line.strip("REACTION")
    tmp  = tmp1.split(' ')
    print tmp[-3]
    f1.write(tmp[-3])
    f1.write("\t")
    tmp1 = tmp[-1].strip("\n")
    f1.write(tmp[-1])

f1.close()
