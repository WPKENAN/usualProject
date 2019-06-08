from min_hash import *
import matplotlib.pyplot as plt
import pandas as pd

import numpy as np


def mergeCsv(maxLines=500):
    csvList=['./data/hzqso_ssw_hw.csv','./data/galaxy_ssw1_hw.csv','./data/mstar_ssw_hw.csv','./data/qso_ssw_hw.csv','./data/star_ssw_hw.csv']

    out=open("./data/mergeCsv.csv",'w')
    for path in csvList:
        count=0;
        lines=open(path).readlines()
        for line in lines:
            count += 1;
            if count>maxLines:
                break
            line=line.strip('\n').strip(',')
            out.write(line+",{}\n".format(path.split('/')[-1].split('.')[0]))


    out.close()





def readCsv(csvPath):
    data=pd.read_csv(csvPath,header=-1);

    print(data.values[:,[0,-1]])
    return data.values[:,[0,-1]],data.values[:,1:-1]

if __name__=="__main__":
    mergeCsv(maxLines=300)

    name=[]

    # data = readCsv('./data/hzqso_ssw_hw.csv')
    # data = readCsv('./data/galaxy_ssw1_hw.csv')
    name,data = readCsv("./data/mergeCsv.csv")

    # data = readCsv('./data/qso_ssw_hw.csv')
    # data = readCsv('./data/star_ssw_hw.csv')

    # plt.plot(data[:,-1])
    # plt.show()
    # print(np.min(data[:, -1]))
    # print(np.max(data[:,-1]))



    # data.dtype='int'
    # print(type(data))
    # print(data)
    # data=data.astype('float')
    # data=np.round(data)
    # data = data.astype('int')
    # print(data)
    # x=[]
    # print(sum(data[:,-1]==0))
    # print(len(np.unique(data[:,-1])))
    # for i in data[:,-3:-1]:
    #     for j in i:
    #         if j!=0:
    #             x.append(j)
    #
    # # print(x)
    # plt.hist(x,bins=range(-50,50,1))
    # plt.show()

    # 输出你的查询序列，和样本真实类别
    inquiry = data[-1, :];
    inquiryName = name[-1, :];
    data=np.vstack((data,inquiry))
    name=np.vstack((name,inquiryName))
    # print(data)

    data=data.astype('float')
    data=np.round(data)
    data = data.astype('int')

    dictValueSet=set()
    for i in data:
        for j in i:
            dictValueSet.add(int(j))

    print(len(dictValueSet))
    dictValueList={}
    i=0
    for key in dictValueSet:
        dictValueList[key]=i
        i=i+1
    print(i)

    dataSet=np.zeros((data.shape[0],len(dictValueSet)))
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i,j] in dictValueList:
                # print(dictValueList[data[i,j]])
                dataSet[i,dictValueList[data[i,j]]]=1;

    print("over")

    print(dataSet.shape)
    result = nn_search(dataSet.tolist(), dataSet[-1,:].tolist(),5,3)
    print(result)
    rightCount=0;
    for i in result:
        if name[i,1]==inquiryName[1]:
            rightCount+=1;

    print("{} / {} = {}".format(rightCount-1,len(result)-1,(rightCount-1)/(len(result)-1)))







