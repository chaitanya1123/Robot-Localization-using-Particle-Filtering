#!/usr/bin/env python
import IPython
import pdb
import random
import numpy as np
#<<<<<<< HEAD
import random
#from mapParser import parser
#=======
#>>>>>>> master

def resampleParticles(X, weights):
	N = len(X)
	XNew = np.zeros(X.shape)

	k = 0
	sumWeights=0
	for i in range(N):
		sumWeights += weights[i]

#<<<<<<< HEAD
	normWeights = (weights*1.0)/sumWeights
	r = np.random.uniform(0,1.0/N)
#=======
	normWeights = weights*1.0/sumWeights
	r = random.uniform(0,1.0/N)
#>>>>>>> master
	c = normWeights[0]
	i = 0
	for m in range(N): 
		u = r + (m)*(1.0/N)
 		while u > c:
 			i = i + 1
 			c = c + (1.0*normWeights[i])
 		XNew[k] = X[i]
 		k=k+1
	return XNew

#<<<<<<< HEAD

	
#if __name__ == "__main__": 
#	main()
#=======
'''def main():
	X = np.array([[7,5,4],[1,2,5],[4,5,9],[5,6,3.4],[0.3,4,6]])
	w = np.array([1,20,30,40,100])
	resampleParticles(X,w)

if __name__ == "__main__": 
	main()'''
#>>>>>>> master
