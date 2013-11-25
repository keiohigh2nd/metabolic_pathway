#!/usr/bin/python
# coding: UTF-8
 
f = open('module_20101013')
lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
f.close()
# lines2: リスト。要素は1行の文字列データ

f1 = open("node.txt", 'w')

i = 0
j = 0
for line in lines2:
    #From Reaction to COMPOUND
    if line.find("REACTION") != -1:
      f1.write(line)
      j += 1

    if line.find("COMPOUND") != -1:
      j = 0

    if j == 1:
      f1.write(line)

f1.close()
