#------------------------------------------------------------------------------------
#--------------------Implemented the sample odometry motion model--------------------
#------------------------------------------------------------------------------------

import random
import math
import numpy as np
import gridFunctions
import IPython

def motionModel(uCurrent, uPrev, xPrev, alpha):
    xCurrent = np.zeros(xPrev.shape) #Initialize

    #Calc deltas, deltacaps, and x,y,theta
    deltaRot1 = math.atan2(uCurrent[1] - uPrev[1], uCurrent[0] - uPrev[0]) - uPrev[2]
    deltaTrans = math.sqrt((uCurrent[0] - uPrev[0]) ** 2 + (uCurrent[1] - uPrev[1]) ** 2)
    deltaRot2 = uCurrent[2] - uPrev[2] - deltaRot1
    # print "odom1: " + str(deltaRot1)
    # print "odom2: " + str(deltaTrans)
    # print "odom3: " + str(deltaRot2)

    # print "rot1: " + str(alpha[0]*deltaRot1 + alpha[1]*deltaTrans)
    trueRot1 = deltaRot1 - sample(0, alpha[0] * math.fabs(deltaRot1) + alpha[1] * math.fabs(deltaTrans))

    # print "trans: " + str(alpha[2]*deltaTrans + alpha[3]*(deltaRot1 + deltaRot2))
    trueTrans = deltaTrans - sample(0, alpha[2] * math.fabs(deltaTrans) + alpha[3] * (
    math.fabs(deltaRot1) + math.fabs(deltaRot2)))

    # print "rot2: " + str(alpha[0]*deltaRot2 + alpha[1]*deltaTrans)
    trueRot2 = deltaRot2 - sample(0, alpha[0] * math.fabs(deltaRot2) + alpha[1] * math.fabs(deltaTrans))

    xCurrent[0] = xPrev[0] + trueTrans * math.cos(xPrev[2] + trueRot1)
    xCurrent[1] = xPrev[1] + trueTrans * math.sin(xPrev[2] + trueRot1)
    xCurrent[2] = xPrev[2] + trueRot1 + trueRot2
    # xCurrent[2] = (xCurrent[2] + (- 2*np.pi)*(xCurrent[2] > np.pi) + (2*np.pi)*(xCurrent[2] < -np.pi))
    return xCurrent


def sample(mu, sigma):
    return np.random.normal(mu, sigma)


def motionModelMap(uCurrent, uPrev, xPrev, alpha, m, resolution):
    while (1):
        xCurrent = motionModel(uCurrent, uPrev, xPrev, alpha)
        if (gridFunctions.checkLimits(xCurrent, resolution, m.shape)):
            pi = gridFunctions.occupancy(xCurrent, resolution, m)
            if pi > 0.8:
                break
        return xCurrent
