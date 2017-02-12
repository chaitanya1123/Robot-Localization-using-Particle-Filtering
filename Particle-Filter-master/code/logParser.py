#!/usr/bin/env python
import os.path
import numpy as np
import matplotlib.pyplot as plt

def parser():
	OData = []
	LData = []
	basePath = os.path.dirname(__file__)
	filePath = os.path.abspath(os.path.join(basePath,"..","data","log","robotdata1.log"))
	f = open(filePath,"r")
	#with open('robotdata1.log') as f:
	lines = f.read().splitlines()
	f.close()

	for i,line in enumerate(lines):
		if lines[i][0] == 'L':
			l = lines[i].split()
			LData.append(float(l[x]) for x in range(1,len(l)))

		if lines[i][0] == 'O':
			l = lines[i].split()
			OData.append(float(l[x]) for x in range(1,len(l)))

	LData = np.array(LData)
	OData = np.array(OData)


	return OData, LData

def main():
	OData, LData = parser()

if __name__ == "__main__": 
	main()
