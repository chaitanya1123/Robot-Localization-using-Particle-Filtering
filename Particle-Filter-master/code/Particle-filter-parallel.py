#!/usr/bin/env python
import numpy as np
import logParser
import mapParser
import motionModel
import gridFunctions
import measurementModel
import resample
import IPython
import matplotlib.pyplot as plt
from multiprocessing import Pool
import particleFitler

class particleFilter(object):
    """docstring for particleFilter"""
    #def __init__(self, m, laserData, odomData, mapData, resolution, numParticles, XInitial, alpha, downSample, offset, minDist):
    def __init__(self, m, laserData, odomData, mapData, resolution, numParticles, XInitial, alpha, downSample, offset):
        self.OData = odomData
        self.LData = laserData
        self.occGrid = mapData
        self.resolution = resolution
        self.N = numParticles
        self.XInitial = XInitial
        self.alpha = alpha
        self.downSample = downSample
        self.offset = offset
        #self.minDist = minDist
        XCurrent = self.XInitial
        self.m = m
        plt.imshow(self.m, cmap = 'gray')
        plt.ion()
        self.scat = plt.quiver(0,0,1,0)
        #back = self.LData.shape[0]-1
        back = len(self.LData)-1
        for i in range(42,200):
            #print "time " + str(i)
            XPrev = XCurrent
            #IPython.embed()
            uPrev = self.OData[i]
            uCurrent = self.OData[i+1]
            #print uCurrent
            #zCurrent = self.LData[i+1, 6:-1]
            zCurrent = self.LData[i + 1][6:-1]
            self.visualize(XCurrent, self.resolution)
            XCurrent = self.particleFilterAlgo(XPrev, uCurrent, uPrev, zCurrent)


    def particleFilterAlgo(self, XPrev, uCurrent, uPrev, zCurrent):
        XCurrent = np.zeros(XPrev.shape)
        XCurrentBar = XPrev
        wtCurrent = np.ones(self.N)
        for n in range(self.N):
            if not np.array_equal(uCurrent[0:3], uPrev[0:3]):
                #while (gridFunctions.checkLimits(XCurrentBar[n], self.resolution, self.occGrid.shape)):
                    #occ = gridFunctions.occupancy(XCurrentBar[n], self.resolution, self.occGrid)
                    #if (occ>0.8):
                XCurrentBar[n] = motionModel.motionModel(uCurrent, uPrev, XPrev[n], self.alpha)
                    #if not (gridFunctions.checkLimits(XCurrentBar[n], self.resolution, self.occGrid.shape)):
                        #break

                #print XCurrentBar[n]
            #wtCurrent[n] = measurementModel.likelihoodRangeFinderModel(zCurrent, XCurrentBar[n], self.occGrid, self.downSample, self.resolution, self.offset, self.minDist)
            wtCurrent[n] = measurementModel.beamRangeFinderModel(zCurrent, XCurrentBar[n], self.occGrid,self.downSample, self.resolution, self.offset)
            #XCurrentBar[n] = np.concatenate((xCurrent, wtCurrent), axis = 1)
            #print "wt: ", wtCurrent[n]
        XCurrent = resample.resampleParticles(XCurrentBar, wtCurrent)
        #IPython.embed()
        #print XCurrent
        return XCurrent

    def visualize(self, X, res):
        self.scat.remove()
        y = np.floor(X[:,0]/res)
        x = np.floor(X[:,1]/res)
        u = np.cos(X[:,2])
        v = np.sin(X[:,2])
        self.scat = plt.quiver(x,y,u,v, edgecolor = 'k', facecolor = 'r')
        plt.pause(0.001)
        #plt.show()

def main():
    odomData, laserData = logParser.parser()
    #minDist = np.loadtxt('min_d.dat', delimiter=' ')
    m, mapData, global_mapsize_x, global_mapsize_y, resolution, autoshifted_x, autoshifted_y = mapParser.parser()
    numParticles = 1000
    particleSize = 3
    downSample = 90
    offset = 25
    XInitial = np.zeros([numParticles,particleSize])

    for i in range(numParticles):
        while 1:
            # XInitial[i] = np.array([3900, 4000, 0])
            XInitial[i] = np.array([np.random.uniform(0, global_mapsize_x), np.random.uniform(0, global_mapsize_y),
                                    np.random.uniform(-1 * np.pi, np.pi)])
            occ = gridFunctions.occupancy(XInitial[i], resolution, mapData)
            if occ > 0.8:
                break

    pf = []
#    for i in range(numParticles):
#           XInitial[i] = np.array([np.random.uniform(0, global_mapsize_x), np.random.uniform(0, global_mapsize_y), np.random.uniform(-1*np.pi, np.pi)])
    for j in range(numParticles//numWorkers):
        for i in range(numWorkers):
            alpha = np.array([0.00001,0.00001,0.01,0.01])
            args = [m, laserData, odomData, mapData, resolution, numWorkers, XInitial, alpha, downSample, offset]
            #pf = particleFilter(m, laserData, odomData, mapData, resolution, numParticles, XInitial, alpha, downSample, offset, minDist)
            pf[j] = pool.apply_async(particleFilter, args)
            #pf = [pool.apply_async(particleFilter, args) for i in range(numWorkers)]

if __name__ == "__main__":
    numWorkers = 10
    pool = Pool(processes=numWorkers)
    main()