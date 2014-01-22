
def visualize_row(line):
	res = []
	if line[2] and line[3] == 0:
		return
	else:
		for i in len(line):
			if i*4 > len(line):
				break
			else:
				if line[i*4].find("C0") != -1:
					top = line[i*4+1]
					bottom = line[i*3+2]
					f.write(line[i*4])
					f.write("\t")
					f.write(float(bottom/top))
			
		

if __name__ == "__main__": 
	f = open("result2.txt","r")
	lines = f.readlines()
	f.close()

	for x in line:
		visualize_row(x)
