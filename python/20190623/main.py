import os
import numpy as np

#读取数据返回low_high
def readData(path):
    contents=open(path).readlines();
    contents=contents[1:]
    # print(len(contents))
    low_high=[]
    for i in range(1,len(contents)):
        line=contents[i].strip('\n');
        line=line.split(' ')
        # print(line)
        low_high.append([float(line[1]),float(line[2])])

    low_high=np.array(low_high)
    # print(low_high)
    # print(low_high.shape)

    return low_high


#计算两组值的关联系数
def calP(arr1,arr2):
    # avg1=np.mean(arr1);
    # avg2=np.mean(arr2);

    var1=np.var(arr1)
    var2=np.var(arr2)
    cov = np.cov(arr1, arr2);  # 协方差矩阵
    p=cov[0,1]/np.sqrt(var1*var2)#相关系数
    # print(cov)
    # print(p)
    return var1,var2,cov[0,1],p


if __name__=="__main__":
    globaLFolder="./data/Global"
    localFolder="./data/Local"
    files=os.listdir(globaLFolder);

    outfile=open("result.csv",'w')
    outfile.write("DAT,low_varGlobal,low_varLocal,low_cov,low_p,high_varGlobal,high_varLocal,high_cov,high_p\n")
    #遍历文件
    for file in files:
        globalData=readData(os.path.join(globaLFolder,file))
        localData=readData(os.path.join(localFolder, file))

        #计算low
        low=calP(globalData[:,0],localData[:,0])

        #计算high
        high=calP(globalData[:, 1], localData[:, 1])

        outfile.write("{},{},{},{},{},{},{},{},{}\n".format(file,low[0],low[1],low[2],low[3],high[0],high[1],high[2],high[3]));


