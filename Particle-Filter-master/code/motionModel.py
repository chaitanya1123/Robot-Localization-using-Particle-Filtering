#!/usr/bin/env python
import random
import math
import numpy as np
import gridFunctions
import IPython

def motionModel(uCurrent, uPrev, xPrev, alpha):
	xCurrent = np.zeros(xPrev.shape)
	#IPython.embed()

	odomRot1 = math.atan2(uCurrent[1] - uPrev[1], uCurrent[0]- uPrev[0]) - uPrev[2]
	odomTrans = math.sqrt((uCurrent[0] - uPrev[0])**2 + (uCurrent[1] - uPrev[1])**2)
	odomRot2 = uCurrent[2] - uPrev[2] - odomRot1
	#print "odom1: " + str(odomRot1)
	#print "odom2: " + str(odomTrans)
	#print "odom3: " + str(odomRot2)

	#print "rot1: " + str(alpha[0]*odomRot1 + alpha[1]*odomTrans)
	trueRot1 = odomRot1 - sample(0, alpha[0]*math.fabs(odomRot1) + alpha[1]*math.fabs(odomTrans))

	#print "trans: " + str(alpha[2]*odomTrans + alpha[3]*(odomRot1 + odomRot2))
	trueTrans = odomTrans -  sample(0, alpha[2]*math.fabs(odomTrans) + alpha[3]*(math.fabs(odomRot1) + math.fabs(odomRot2)))

	#print "rot2: " + str(alpha[0]*odomRot2 + alpha[1]*odomTrans)
	trueRot2 = odomRot2 - sample(0, alpha[0]*math.fabs(odomRot2) + alpha[1]*math.fabs(odomTrans))

	xCurrent[0] = xPrev[0] + trueTrans * math.cos(xPrev[2] + trueRot1)
	xCurrent[1] = xPrev[1] + trueTrans * math.sin(xPrev[2] + trueRot1)
	xCurrent[2] = xPrev[2] + trueRot1 + trueRot2
	#xCurrent[2] = (xCurrent[2] + (- 2*np.pi)*(xCurrent[2] > np.pi) + (2*np.pi)*(xCurrent[2] < -np.pi))
	#IPython.embed()
	return xCurrent

def sample(mu, sigma):
	return np.random.normal(mu, sigma)

def motionModelMap(uCurrent, uPrev, xPrev, alpha, m, resolution):
	#\while (1):
		xCurrent = motionModel(uCurrent, uPrev, xPrev, alpha)
	#	if (gridFunctions.checkLimits(xCurrent, resolution, m.shape)):
	#		pi = gridFunctions.occupancy(xCurrent, resolution, m)
	#		if pi>0.8:
	#			break
		return xCurrent
