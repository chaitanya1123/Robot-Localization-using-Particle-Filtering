#------------------------------------------------------------------------------------
#----Functions for checking the prob of occupancy and Limits in the map--------------
#------------------------------------------------------------------------------------
import numpy as np 
import math
import IPython

def occupancy(x, resolution, map):
    xMap = int(math.floor(x[0]//resolution))
    yMap = int(math.floor(x[1]//resolution))

    return 1-map[xMap, yMap]

def checkLimits(x, resolution, mapSize):
    xMap = math.floor(x[0]//resolution)
    yMap = math.floor(x[1]//resolution)
    if (xMap >= 0) and (xMap < mapSize[0]) and (yMap >= 0) and (yMap < mapSize[1]):
        return True
    else:
        return False
