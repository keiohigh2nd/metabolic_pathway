"""
This script is to read affmetrix GSEA file and convert it to the gene,fold_change
"""

f = open("All_GSEA.csv")
data = f.read()
f.close()

f1 = open("t_All_GSEA.csv","w")


lines = data.split("\r")
for x in lines:
	tmp = x.split(",")
	if tmp[1].find("GEN=") != -1:
		tmp_t = tmp[1].split("/")
		for y in tmp_t:
			if y.find("GEN") != -1:
				f1.write(y.strip("GEN="))
				f1.write(",")	
				foldchange = float(tmp[-1])/float(tmp[-2])
				f1.write(str(foldchange))
				f1.write("\n")	
f1.close()


				
