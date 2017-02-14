#------------------------------------------------------------------------------------
#--------------------Robot Localization using Particle Filtering---------------------
#----------------------------Lab 1 - CS 8803 STR-------------------------------------
#-------------Chaitanya R. Maniar, Sampada Upasani, Pushyami Shandilya---------------
#------------------------------------------------------------------------------------

import numpy as np
import logParser
import mapParser
import motionModel
import gridFunctions
import measurementModel
import resample
import IPython
import matplotlib.pyplot as plt
import os.path



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
        #XCurrentBar = self.XInitial
        self.m = m
        plt.imshow(self.m, cmap = 'gray')
        plt.ion()
        self.scat = plt.quiver(0,0,1,0)
        #back = self.LData.shape[0]-1
        back = len(self.LData)-1
        #Run Particle filter
        for i in range(back):
            print("time " + str(i))
            XPrev = XCurrent

            uPrev = self.OData[i]
            uCurrent = self.OData[i+1]
            #print uCurrent
            #zCurrent = self.LData[i+1, 6:-1]
            zCurrent = self.LData[i + 1][6:-1]
            basePath = os.path.dirname(__file__)
            self.visualize(XCurrent, self.resolution, i, basePath)
            XCurrent = self.particleFilterAlgo(XPrev, uCurrent, uPrev, zCurrent, i)


    def particleFilterAlgo(self, XPrev, uCurrent, uPrev, zCurrent, i):
        #Init Step
        XCurrent = np.zeros(XPrev.shape)
        XCurrentBar = XPrev
        wtCurrent = np.ones(self.N)
        print(uCurrent[0:3])
        #Only run the motion model and measurement model for significant motion.
        if (uCurrent[0:3] != uPrev[0:3]):
            for n in range(self.N):
                #while (gridFunctions.checkLimits(XCurrentBar[n], self.resolution, self.occGrid.shape)):
                    #occ = gridFunctions.occupancy(XCurrentBar[n], self.resolution, self.occGrid)
                    #if (occ>0.8):
                XCurrentBar[n] = motionModel.motionModel(uCurrent, uPrev, XPrev[n], self.alpha)#Run Motion Model to get Xs
                np.savetxt("x-after-mom.txt", XCurrentBar, delimiter=" ")

                    #if not (gridFunctions.checkLimits(XCurrentBar[n], self.resolution, self.occGrid.shape)):
                        #break
                #print(XCurrentBar[n])
            #wtCurrent[n] = measurementModel.likelihoodRangeFinderModel(zCurrent, XCurrentBar[n], self.occGrid, self.downSample, self.resolution, self.offset, self.minDist)
                #Run Measurement Model for weights
                wtCurrent[n] = measurementModel.beamRangeFinderModel(zCurrent, XCurrentBar[n], self.occGrid,self.downSample, self.resolution, self.offset)
                np.savetxt("w-after-meam.txt", wtCurrent, delimiter=" ")
            #XCurrentBar[n] = np.concatenate((XCurrent, wtCurrent), axis = 1)
                #print ("wt: ", wtCurrent)
        #if not np.array_equal(XCurrentBar, XPrev):
            #Resampling step
            XCurrent = resample.resampleParticles(XCurrentBar, wtCurrent)
            np.savetxt("x-after-resample.txt", XCurrent, delimiter=" ")
            return XCurrent
        #If Significant motion has happened, move, measure, resample. Else return.
        #print(XCurrent)
        return XCurrentBar

    def visualize(self, X, res, i,basePath):#Method for visualizing particles. Arrows represent orientation direction
        self.scat.remove()
        y = np.floor(X[:,0]/res)
        x = np.floor(X[:,1]/res)
        u = np.cos(X[:,2])
        v = np.sin(X[:,2])
        plt.imshow(self.m, cmap='gray')
        plt.ion()
        self.scat = plt.quiver(x, y, u, v, color='red', width=0.005)
        plt.savefig(os.path.join(basePath, "..", "images", 'fig {0}.jpg'.format(i)))
        plt.pause(0.00001)
        #plt.show()



def main():
    odomData, laserData = logParser.parser()

    m, mapData, global_mapsize_x, global_mapsize_y, resolution, autoshifted_x, autoshifted_y = mapParser.parser()
    numParticles = 100
    particleSize = 3
    downSample = 10
    offset = 25
    XInitial = np.zeros([numParticles,particleSize])

#    for i in range(numParticles):
#           XInitial[i] = np.array([np.random.uniform(0, global_mapsize_x), np.random.uniform(0, global_mapsize_y), np.random.uniform(-1*np.pi, np.pi)])

    for i in range(numParticles):
        while 1:
            #XInitial[i] = np.array([3900, 4000, 0])
            XInitial[i] = np.array([np.random.uniform(0, global_mapsize_x), np.random.uniform(0, global_mapsize_y),
                                   np.random.uniform(-1 * np.pi, np.pi)]) #Init N particles with random pose and orientation
            occ = gridFunctions.occupancy(XInitial[i], resolution, mapData) #Check Occupancy
            if occ > 0.8:
                break
    alpha = np.array([0.05, 0.05, 0.1, 0.1]) #Parameters for motion model
    #pf = particleFilter(m, laserData, odomData, mapData, resolution, numParticles, XInitial, alpha, downSample, offset, minDist)
    pf = particleFilter(m, laserData, odomData, mapData, resolution, numParticles, XInitial, alpha, downSample, offset)

if __name__ == "__main__":
    main()