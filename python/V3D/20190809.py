import os
import sys
import cv2 as cv
import numpy as np
from sklearn.decomposition import PCA

# 零均值化
def zeroMean(dataMat):
    meanVal = np.mean(dataMat, axis=0)  # 按列求均值，即求各个特征的均值
    newData = dataMat - meanVal
    return newData, meanVal


def pcaMy(dataMat, n):
    newData, meanVal = zeroMean(dataMat)
    covMat = np.cov(newData, rowvar=0)  # 求协方差矩阵,return ndarray；若rowvar非0，一列代表一个样本，为0，一行代表一个样本
    # print(covMat)
    eigVals, eigVects = np.linalg.eig(np.mat(covMat))  # 求特征值和特征向量,特征向量是按列放的，即一列代表一个特征向量
    # print(eigVals)
    # print(eigVects)
    eigValIndice = np.argsort(eigVals)  # 对特征值从小到大排序
    # print(eigValIndice)
    n_eigValIndice = eigValIndice[-1:-(n + 1):-1]  # 最大的n个特征值的下标
    n_eigVect = eigVects[:, n_eigValIndice]  # 最大的n个特征值对应的特征向量
    print(eigVects[:,:])
    lowDDataMat = newData * n_eigVect  # 低维特征空间的数据
    reconMat = (lowDDataMat * n_eigVect.T) + meanVal  # 重构数据
    return lowDDataMat, reconMat



if __name__=="__main__":
    x = np.array([2.5, 0.5, 2.2, 1.9, 3.1, 2.3, 2, 1, 1.5, 200])
    y = np.array([2.9, 0.7, 2.9, 2.2, 3, 2.7, 1.6, 1.1, 1.6, 0.9])
    dataMat=np.vstack((x,y))
    dataMat=dataMat.transpose()
    # print(dataMat)
    lowDDataMat, reconMat=pcaMy(dataMat,2)
    # print(lowDDataMat)
    # for i in range(100*100*100):
    #     print(i)
    #     dataMat=np.random.random((100,3))
    #     # print(dataMat)
    #     # lowDDataMat, reconMat = pca(dataMat, 2)
    #     pca = PCA(n_components=2)
    #     pca.fit(dataMat)
    #     print(pca.components_)
    #     pca.transform(dataMat)
        # pca(dataMat)
    pca = PCA(n_components=1)
    pca.fit(dataMat)
    print(pca.components_)


