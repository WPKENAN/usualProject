import keras
from keras.layers import LSTM
from keras.layers import Dense, Activation
from keras.datasets import mnist
from keras.models import Sequential
from keras.optimizers import Adam
import os
import numpy as np
import scipy.io as scio
import random
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
from keras.callbacks import TensorBoard
from keras.callbacks import ModelCheckpoint
from keras.regularizers import l2
from keras.layers import Dense, Dropout, Activation, Flatten
from createModel import *
#直接全部预测
def predict_point_by_point(allX, allY):
    x_train, y_train, x_test, y_test = loadData(allX, allY)
    model = keras.models.load_model("./0.88_valcounts0.9/best.hdf5")

    predicted = model.predict(x_test)
    print('predicted shape:',np.array(predicted).shape)  #(412L,1L)
    y_pred = np.argmax(predicted, axis=1)
    y_test=np.argmax(y_test, axis=1)
    print(y_pred.shape)
    print(y_test.shape)
    print(target_names)
    print(classification_report(y_test, y_pred, target_names=target_names))

def plotCM(classes, matrix, savname):
    """classes: a list of class names"""
    from pylab import mpl

    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(matrix)
    fig.colorbar(cax)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            ax.text(i, j, str('%.2f' % (matrix[i, j])), va='center', ha='center',fontsize=10,color='r')
    ax.set_xticklabels([''] + classes, rotation=90,fontsize=10)
    ax.set_yticklabels([''] + classes,fontsize=10)
    plt.xlabel("True")
    plt.ylabel("Predice")
    plt.show()



def loadData(allX,allY):
    random.seed(0)
    index = list(range(len(allY)));
    random.shuffle(index)
    allX = allX[index, :]
    allY = allY[index, :]
    val = 0.9
    x_train, y_train = allX[0:int(len(allY) * val), :], allY[0:int(len(allY) * val), :]
    x_test, y_test = allX[int(len(allY) * val):, :], allY[int(len(allY) * val):, :]
    # print(x_train.shape)
    x_train = x_train.reshape(-1, n_step, n_input)
    x_test = x_test.reshape(-1, n_step, n_input)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    file = open("config.txt", 'r').readlines()
    mean = float(file[0].strip('\n').split(',')[0])
    std=float(file[0].strip('\n').split(',')[1])


    # mean = np.mean(x_train)
    # std = np.std(x_train)
    print("Before normalize mean:{} std:{} ".format(mean, std))
    x_train -= mean
    x_train /= std
    print("After normalize mean:{} std:{} ".format(np.mean(x_train), np.std(x_train)))
    x_test -= mean
    x_test /= std
    print(x_train.shape)
    y_train = keras.utils.to_categorical(y_train, n_classes)
    y_test = keras.utils.to_categorical(y_test, n_classes)

    x_train = np.reshape(x_train, (x_train.shape + (1,)))
    x_test = np.reshape(x_test, (x_test.shape + (1,)))
    return x_train,y_train,x_test,y_test

def printMatrix(allX,allY):
    x_test, y_test,x_train, y_train= loadData(allX, allY)
    model = keras.models.load_model("./0.88_valcounts0.9/best.hdf5")
    model.summary()
    predicted = model.predict(x_test)
    print('predicted shape:', np.array(predicted).shape)  # (412L,1L)
    y_pred = np.argmax(predicted, axis=1)
    y_test = np.argmax(y_test,axis=1)
    print(classification_report(y_test, y_pred, target_names=target_names))

    matrix = np.zeros((len(target_names),len(target_names)));
    for index in range(len(y_pred)):
        matrix[int(y_test[index])][int(y_pred[index])]+=1
    # #概率
    # for i in range(len(target_names)):
    #     matrix[:,i]=matrix[:,i]/np.sum(matrix[:,i])

    plotCM(target_names, matrix, "")


weight_decay=0.005
learning_rate = 1e-4
training_iters = 1000
batch_size = 64
display_step = 10

n_input = 40
n_step = 40
n_hidden = 40
n_classes = 0
path="../data/pro1_data"
target_names=sorted(os.listdir(path))
if __name__=="__main__":
    n_classes=len(os.listdir(path))
    # loaddata(path)
    allX = np.load("allX.npy")[:,:1600]
    allY = np.load("allY.npy")
    print(allX.shape)
    print(allY.shape)
    n_input = 40
    n_step = allX.shape[1] // n_input

    # predict(allX,allY)
    # predict_point_by_point(allX,allY)
    printMatrix(allX,allY)

# 2 804.0
# 3 536.0
# 4 402.0
# 6 268.0
# 8 201.0
# 12 134.0
# 24 67.0
# 67 24.0
# 134 12.0
# 201 8.0
# 268 6.0
# 402 4.0
# 536 3.0
# 804 2.0