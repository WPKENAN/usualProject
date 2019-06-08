import scipy.io as scio
import os
import numpy as np


if __name__=='__main__':
    path="./data"
    count=0
    for file in os.listdir(path):
        dataFile = os.path.join(path,file)
        data = scio.loadmat(dataFile)
        print(data.keys())
        keys=[]
        for key in data.keys():
            keys.append(key)

        print(np.transpose(data[keys[-1]]).shape)
        x=np.transpose(data[keys[-1]])
        y=np.zeros((x.shape[0],1))+count

        if count==0:
            allX=x;
            allY=y;
        else:
            allX=np.vstack((allX,x[:800,:]))
            allY = np.vstack((allY, y[:800,:]))
        count=count+1


