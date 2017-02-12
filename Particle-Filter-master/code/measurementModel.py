import numpy as np
import sys
import time
import math
import mapParser
import matplotlib.pyplot as plt
import gridFunctions
import IPython
import logParser

# variables :
#LaserReadings = [x, y, theta, xl, yl, thetal, r1......r180]
#
# parameters :
#zHit, zRand, zShort, zMax, sigmaHit, lambdaShort
#zMax = 5000
#L = 25

zRand = 0.033
zHit = 0.9
zShort = 0.033
zMax = 0.034
sigmaHit = 5
lambdaShort = 0.5
laserMax = 1000

def measurementToMap(zt, xt, n, L):
    #IPython.embed()
    zt_map = np.empty([n])
    #print zt_map.shape
    for k in range(0, zt.shape[0], zt.shape[0]/n):
        theta = xt[2]
        phi = -90 + k      #ztk[2]
        xt_k = xt[0] + L*math.cos(theta) + zt[k]*math.cos(theta + phi)
        yt_k = xt[1] + L*math.sin(theta) + zt[k]*math.sin(theta + phi)
        #IPython.embed()
        zt_map[k*n/zt.shape[0]] = math.sqrt(xt_k**2 + yt_k**2)
    #print zt_map
    #IPython.embed()
    return zt_map

def get_pHit(ztk, zt_true):
    if ztk >= 0 and ztk <= laserMax:
        #pHit = np.random.normal(zt_true, sigmaHit)
        #print "ztk", ztk
        #print "zt_true", zt_true
        pHit = -0.5*math.log(2*math.pi*(sigmaHit**2)) - 0.5*((ztk-zt_true)**2)/(sigmaHit**2)
        pHit = math.exp(pHit)
        #pHit = math.exp((-0.5*((ztk - zt_true)**2)/(sigmaHit**2)))/math.sqrt(2*math.pi*sigmaHit**2)
        #pHit = max(min((ztk - zt_true + sigmaHit)/(sigmaHit**2), (zt_true - ztk + sigmaHit)/(sigmaHit**2)),0)
        return pHit
    else:
        return 0


def get_pShort(ztk, zt_true):
    if (ztk >= 0 and ztk <= zt_true):
        #eta = 1.0/(1-math.exp(-lambdaShort*zt_true))
        pShort = math.log(lambdaShort) - lambdaShort*ztk
        pShort = math.exp(pShort)
        #pShort = lambdaShort * math.exp(-lambdaShort*ztk)
        return pShort
    else:
        return 0

def get_pMax(ztk):
    if ztk == laserMax:
        return zMax
    else:
        return 0

def get_pRand(ztk):
    if ztk >= 0 and ztk < laserMax:
        return 1.0*zRand/laserMax
    else:
        return 0

def beamRangeFinderModel(zt, xt, m, n, resolution, L):
    q = 1
    #zMax = 2000
    zt_map = measurementToMap(zt, xt, n, L)
    #zt_true = [0]*len(zt)
    zt_true, angs = rayCasting(xt, m, laserMax, n, resolution)        # ray casting step
    #x = xt[0] + zt_true*cos()
    for k in range(len(zt_map)):
        zt_true[k] = math.sqrt((xt[0] + zt_true[k] * math.cos(xt[2]+angs[k]))**2 + (xt[1] + zt_true[k] * math.sin(xt[2]+angs[k]))**2)
        #print zt_map[k], zt_true[k]
        #print get_pHit(zt_map[k], zt_true[k])
        #print get_pShort(zt_map[k], zt_true[k])
        #print get_pMax(zt_map[k])
        #print get_pRand(zt_map[k])
        p = zHit * get_pHit(zt_map[k], zt_true[k])# + get_pShort(zt_map[k], zt_true[k]) + get_pMax(zt_map[k]) + get_pRand(zt_map[k])
        #print "p: ", p
        q = p + q
        p = zShort * get_pShort(zt_map[k], zt_true[k])
        q = p + q
    #print "here"
    return q


def rayCasting(xt, m, laserMax, n, resolution):
    #pixeltocm = 10
    xc = xt[0]
    yc = xt[1]
    if gridFunctions.occupancy(xt, resolution, m) == 0:
        lrange = np.zeros(n)
        #print lrange
        return lrange

    #plt.imshow(m, cmap = 'gray', extent = [0,800,800,0])
    #plt.plot(1.0*xc/10,1.0*yc/10,'bo')

    lrange = np.zeros(n)
    angs = np.zeros(n)
    thetastep = np.pi/n
    for i in range(n):
        theta = -(np.pi/2) + thetastep * i
        r = np.linspace(0, laserMax, 1000)
        x = xc + (r[:]*math.cos(theta))
        y = yc + (r[:]*math.sin(theta))
        t = 0
        temp = []
        for k in range(len(x)):
            if not gridFunctions.checkLimits(np.array([x[k],y[k],t]), resolution, m.shape):
                temp.append(k)
        if (temp):
            x = np.delete(x, temp)
            y = np.delete(y, temp)

        # plot (x,y)
        #plt.plot(x,y,'go')

        xint = (x/resolution).astype(int)
        yint = (y/resolution).astype(int)

        b = []
        for j in range(len(xint)):
            b.append(m[yint[j]][xint[j]])
        ind = np.where(np.array(b) == 0)
        #if i is 69:
            #IPython.embed()
        #print b
        #print ind

        if ind[0].size:
            xb = x[ind[0][0]]
            yb = y[ind[0][0]]
            #plt.plot(1.0*xb/10,1.0*yb/10,'yo')
            dist = math.sqrt((xc-xb)**2 + (yc-yb)**2)
            phi = math.atan2((yc-yb), (xc-xb))
            angs[i] = phi
            lrange[i] = dist

    #plt.show()
    #print lrange
    #IPython.embed()
    return lrange, angs



def likelihoodRangeFinderModel(zt, xt, m, n, resolution, L, minDist):
    q = 1
    for k in range(0, zt.shape[0], zt.shape[0]/n):
        theta = xt[2]
        phi = -90 + k      #ztk[2]
        xt_k = xt[0] + L*math.cos(theta) + zt[k]*math.cos(theta + phi)
        yt_k = xt[1] + L*math.sin(theta) + zt[k]*math.sin(theta + phi)
        zt_map = math.sqrt(xt_k**2 + yt_k**2)
        if (zt_map<laserMax):
            xint = (xt_k/resolution).astype(int)
            yint = (yt_k/resolution).astype(int) 
            #IPython.embed()           
            dist = minDist[xint,yint]
            q = q * (zHit*(dist)/(dist+sigmaHit**2) + (zRand/zMax))
    return q 


def main():
    m, z, global_mapsize_x, global_mapsize_y, resolution, autoshifted_x, autoshifted_y = mapParser.parser()
    OData, LData = logParser.parser()
    xt = np.array([4000,4000,np.pi])
    n= 100
    #measurementToMap(LData[0,6:-1], xt, n, L)
    
    #q = beamRangeFinderModel(LData[0,6:-1], xt, m, n)
    #IPython.embed()
    #print q

    
    rayCasting(xt, z, laserMax, n, 10)

#main()





