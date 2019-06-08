from e2LSH import *
from test_helper import *
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

    # print(data.values[:,[0,-1]])
    return data.values[:,[0,-1]],data.values[:,1:-1]

def readOnlyOne(csvPath):
    data = pd.read_csv(csvPath, header=-1);
    print("随机选中的查询的数据")
    quiryIndex = np.random.randint(len(data))
    print(quiryIndex,[data.values[quiryIndex,0]])
    # print(data.values[quiryIndex,:-1])
    return [data.values[quiryIndex,0]],data.values[quiryIndex,1:-1].tolist()

if __name__ == "__main__":
    T=10
    acc=0
    for t in range(T):
        maxLines=500
        mergeCsv(maxLines)
        name = []
        name, data = readCsv("./data/mergeCsv.csv")

        C = pow(2, 32) - 5
        dataSet = data.tolist()
        # 输出你的查询序列，和样本真实类别
        quiryPath='./data/hzqso_ssw_hw.csv'
        inquiryName,inquiry=readOnlyOne(quiryPath)
        inquiryName.append(quiryPath.split('/')[-1].split('.')[0])
        # print(inquiryName, inquiry)

        result = nn_search(dataSet, inquiry, k=20, L=5, r=4, tableSize=50)
        # print(result)
        # for index in result:
        #     print(name[index])
        #     print(euclideanDistance(dataSet[index], inquiry))

        rightCount=0
        for i in result:
            if name[i,1]==inquiryName[1]:
                rightCount+=1;

        if len(result)!=0:
            print("{} / {} = {}".format(rightCount, len(result), (rightCount) / (len(result))))
            acc+=rightCount / len(result)

    print('整体正确率:{}'.format(acc/T))