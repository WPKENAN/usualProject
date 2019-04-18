from __future__ import print_function
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (precision_score, recall_score,
                             f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py


traindata = pd.read_csv('..\\UNSW_NB15_training-set.csv')
testdata = pd.read_csv('..\\UNSW_NB15_testing-set.csv')
traindata = pd.get_dummies(data=traindata, columns=['proto', 'service', 'state'])
testdata = pd.get_dummies(data=testdata, columns=['proto', 'service', 'state'])

datatrain=traindata.values;
np.random.shuffle(datatrain)
trainNum=1000
X = datatrain[:trainNum,1:191]
Y = datatrain[:trainNum,0]

datatest=testdata.values;
np.random.shuffle(datatest)
C = datatest[:,0]
T = datatest[:,1:191]

scaler = Normalizer().fit(X)
trainX = scaler.transform(X)

scaler = Normalizer().fit(T)
testT = scaler.transform(T)

y_train = np.array(Y)
y_test = np.array(C)

print(trainX.shape)
print(y_train.shape)

print(testT.shape)
print(y_test.shape)

y_pred=[]
for i in range(testT.shape[0]):
    print(i)
    ####计算欧式距离
    diff=np.tile(testT[i,:],(trainX.shape[0],1))-trainX;
    # print(diff);
    sqdiff = diff ** 2
    # print(sqdiff)
    squareDist = np.sum(sqdiff, axis=1)  ###行向量分别相加，从而得到新的一个行向量
    # print(squareDist)
    dist = squareDist ** 0.5

    ##对距离进行排序
    sortedDistIndex = np.argsort(dist)  ##argsort()根据元素的值从小到大对元素进行排序，返回下标
    # print(sortedDistIndex)

    classCount = {}
    k=10;
    for i in range(k):
        voteLabel = y_train[sortedDistIndex[i]]
        ###对选取的K个样本所属的类别个数进行统计
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1
    ###选取出现的类别次数最多的类别
    maxCount = 0
    for key, value in classCount.items():
        if value > maxCount:
            maxCount = value
            classes = key
    y_pred.append(classes);

# print(y_train)
# print([y_test,y_pred])
accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred , average="binary")
precision = precision_score(y_test, y_pred , average="binary")
f1 = f1_score(y_test, y_pred, average="binary")
print("confusion matrix")
print("----------------------------------------------")
print("accuracy")
print("%.3f" %accuracy)
print("racall")
print("%.3f" %recall)
print("precision")
print("%.3f" %precision)
print("f1score")
print("%.3f" %f1)
cm = metrics.confusion_matrix(y_test, y_pred)
print(cm)
print("==============================================")

outfile=open('result.csv','w');
outfile.write('accuracy,{}\n'.format(accuracy));
outfile.write('recall,{}\n'.format(recall));
outfile.write('precision,{}\n'.format(precision));
outfile.write('f1score,{}\n'.format(f1));
outfile.write('confusion_matrix,{},{},{},{}\n'.format(cm[0,0],cm[0,1],cm[1,0],cm[1,1]));
outfile.close()