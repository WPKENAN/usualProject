import os
import sys
import scipy.io as scio
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import shutil

def readData(path):
    data = scio.loadmat(path)

    # print(data['Category_1_Average_fengxueyingr'])

def readFolder(path):
    fileList=os.listdir(path)
    print(fileList)

    for file in fileList:
        # data=scio.loadmat(os.path.join(path, file))
        # keys=list(data.keys())
        # print(data[keys[3]].shape)
        # print(data[keys[3]].shape)
        # print(data[keys[5]][0])
        # plt.show()
        # img=(data[keys[3]]-np.min(data[keys[3]]))/(np.max(data[keys[3]])-np.min(data[keys[3]]))*255
        # img=cv.equalizeHist(img)
        # print(img)
        # cv.imshow("main",img);
        # cv.waitKey(1000)
        # cv.destroyAllWindows()
        break

def mvFile(path,target='../'):
    fileList = os.listdir(path)
    print(fileList)

    count=0
    print(fileList)

    classes=["diff-true","diff-random","diff-error","diff-lie","easy-true","easy-random","easy-error","easy-lie"]
    classes = ["true", "random", "error", "lie"]
    
    for classe in classes:
        if os.path.exists(os.path.join(target,classe)):
            shutil.rmtree(os.path.join(target,classe))
        os.mkdir(os.path.join(target,classe))
    for file in fileList:
        for classe in classes:
            if classe in file:
                shutil.copy(os.path.join(path,file),os.path.join(target,classe,file))
    print(count)



if __name__=="__main__":
    path="../../data/naodian/rawData"

    # readData(path)
    # readFolder('../../data/naodian')
    # print(os.path.exists(path))

    # a=np.array([1,2,3])
    # a=10
    # import copy
    # # b=copy.deepcopy(a)
    # b=copy.copy(a)
    # # b=11
    # # a.append(10)
    # # b.append([12])
    # # b=a
    # # b[0]=10
    # # print(a,b)
    # # a[0]=11
    # print(id(a),id(b))
    # print(a,b)
    # b[0]=11
    # print(a)
    # print([1,2,3]==[2,2,3])
    # print(a==b)

    # a = [1, 2, 3, 4, ['a', 'b']]  # 原始对象

    # import copy
    # b=a.copy()
    # c=copy.deepcopy(a)
    # a.append(10)
    # a[4].append('c')

    # print(a)
    # print(b)
    # print(c)
    mvFile(path,"../../data/naodian/classes4")
