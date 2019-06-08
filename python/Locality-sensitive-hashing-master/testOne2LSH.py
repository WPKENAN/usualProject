from e2LSH import *
from test_helper import *
import pandas as pd


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

if __name__ == "__main__":
    mergeCsv(maxLines=700)
    name = []
    name, data = readCsv("./data/mergeCsv.csv")

    C = pow(2, 32) - 5
    dataSet = data.tolist()
    # 输出你的查询序列，和样本真实类别
    inquiry = data[-1];
    inquiryName = name[-1, :];

    result = nn_search(dataSet, inquiry, k=20, L=5, r=4, tableSize=50)
    print(result)
    for index in result:
        print(euclideanDistance(dataSet[index], inquiry))

    rightCount=0
    for i in result:
        if name[i,1]==inquiryName[1]:
            rightCount+=1;

    print("{} / {} = {}".format(rightCount, len(result), (rightCount) / (len(result))))