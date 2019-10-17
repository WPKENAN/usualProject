import time
import datetime
import pandas as pd
import numpy as np
import os
import collections

# text = "I'm a hand some boy!"
# frequency = collections.Counter(text.split())
# print(frequency)

# t = time.time()
# print(t)
# print(time.localtime(1466543543))
# dt=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(1466543543))
# timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
# print(timeArray)
# timestamp = time.mktime(timeArray)
#
# print(timestamp)


def readCsv(path):
    df=pd.read_csv(path,header=0)
    # print(df)
    data=df.values
    # print(type(data[0,0]))
    # max_=max(data[:,0])
    # dt=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(max_))
    # timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return data
    # print(dt)
    # print(timeArray)
    # print(type(data[0,0]))
    # data.sort(axis=0)
    # print(data)
    # print(data[data[:,0]<1466638597].shape)
    # return data

def readFolder(folder):
    # pass
    _flag=1;
    for file in os.listdir(folder):
        path=os.path.join(folder,file)
        if _flag:
            data=readCsv(path)
            _flag=0;
        else:
            data=np.vstack((data,readCsv(path)))
        print(data.shape)
    return data
if __name__=="__main__":
    path="./data/_juliannemoore.csv"
    folder="./data"
    # data=readCsv(path)
    data=readFolder(folder)
    # print(data.shape)
    # data=np.vstack((data,data))
    # print(data)
    # print(data.shape)
    for i in range(data.shape[0]):
        data[i,1]=data[i,1].lower()
    df=pd.DataFrame(data)
    df.to_csv("data.csv",index=False,header=False)
    data.sort(axis=0)
