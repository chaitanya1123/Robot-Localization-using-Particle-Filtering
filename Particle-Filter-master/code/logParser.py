#------------------------------------------------------------------------------------
#-------------Method to extract log files into OData and LData-----------------------
#------------------------------------------------------------------------------------
import os.path
import numpy as np
def parser():
    OData = {}
    LData = {}
    basePath = os.path.dirname(__file__)
    filePath = os.path.abspath(os.path.join(basePath,"..","data","log","ascii-robotdata2.log"))
    f = open(filePath,"r")
    #with open('robotdata1.log') as f:
    lines = f.read().splitlines()
    f.close()
    keyL = 0
    keyO = 0
    for i,line in enumerate(lines):
        if lines[i][0] == 'L':
            l = lines[i].split()
            LData[i] = tuple(float(l[x]) for x in range(1,len(l)))
            LData[keyL]=LData[i]
            keyL += 1


        elif lines[i][0] == 'O':
            l = lines[i].split()
            OData[i] = tuple(float(l[x]) for x in range(1,len(l)))
            OData[keyO] = OData[i]
            keyO += 1
    #LData = np.array([LData])
    #OData = np.array([OData])


    return OData, LData

def main():
    OData, LData = parser()

if __name__ == "__main__": 
    main()
