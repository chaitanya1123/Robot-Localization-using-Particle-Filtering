#------------------------------------------------------------------------------------
#-------------------Method to extract the Map & its parameters-----------------------
#------------------------------------------------------------------------------------
import os.path
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import IPython

def parser():
    basePath = os.path.dirname(__file__)
    filePath = os.path.abspath(os.path.join(basePath,"..","data","map","wean.dat"))
    f = open(filePath,"r")
    words = f.read().split()

    m, f2 = [], []
    for i in range(len(words)):
        if words[i] == 'robot_specifications->global_mapsize_x':
            global_mapsize_x = int(words[i+1])
        elif words[i] == 'robot_specifications->global_mapsize_y':
            global_mapsize_y = int(words[i+1])
        elif words[i] == 'robot_specifications->resolution':
            resolution = int(words[i+1])
        elif words[i] == 'robot_specifications->autoshifted_x':
            autoshifted_x = int(words[i+1])
        elif words[i] == 'robot_specifications->autoshifted_y':
            autoshifted_y = int(words[i+1])
        elif words[i] == 'global_map[0]:':
            mapsize_x = int(words[i+1])
            mapsize_y = int(words[i+2])
            m = [[] for t in range(mapsize_x)]
            for x in range(0,mapsize_x):
                for y in range(0,mapsize_y):
                    #m[x].append(float(words[i+3+x+y*mapsize_x]))
                    m[x].append(float(words[i+3+x*mapsize_y+y]))
    m = np.array(m)
    m = np.rot90(m)

    z = np.zeros(m.shape)
    z[m>0.8] = 0
    z[m<0.8] = 1


    m[m==-1] = 0
    m[m==1] = 1
    #plt.imshow(z, cmap = plt.cm.binary)
    #plt.show()
    return m, z, global_mapsize_x, global_mapsize_y, resolution, autoshifted_x, autoshifted_y

    #m = np.array(m)
    #m = np.rot90(m)
    #m= np.transpose(m)
    #plt.imshow(m)
    #plt.show()
    #return m

#def main():
#	m = parser()

#if __name__ == "__main__": 
#	main()
