# coding: utf-8

# import the necessary packages

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
import matplotlib.pyplot as plt
# import  matplotlib
# matplotlib.use("Agg")
# import numpy as np
# import argparse
import random
import cv2
import os
import keras
import sys
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import regularizers


# coding=utf-8
from keras.models import Model
from keras.layers import Input, Dense, BatchNormalization, Conv2D, MaxPooling2D, AveragePooling2D, ZeroPadding2D
from keras.layers import add, Flatten
# from keras.layers.convolutional import Conv2D,MaxPooling2D,AveragePooling2D
from keras.optimizers import SGD
import numpy as np
from keras.callbacks import ModelCheckpoint
from keras.callbacks import TensorBoard
from keras import backend as K
from keras.layers import Conv2D,MaxPool2D
from sklearn import svm
from sklearn.metrics import classification_report


import  numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from sklearn.metrics import roc_curve, auc
import copy

def predict_point_by_point(allX, allY):
    x_train, y_train, x_test, y_test = loadData(allX, allY)
    model = keras.models.load_model("./best.hdf5")

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

def printMatrix(allX,allY):
    x_train, y_train, x_test, y_test = loadData(allX, allY)
    model = keras.models.load_model("./best.hdf5")

    predicted = model.predict(x_test)
    print('predicted shape:', np.array(predicted).shape)  # (412L,1L)
    y_pred = np.argmax(predicted, axis=1)
    y_test = np.argmax(y_test,axis=1)
    print(classification_report(y_test, y_pred, target_names=target_names))

    matrix = np.zeros((len(target_names),len(target_names)));
    for index in range(len(y_pred)):
        matrix[int(y_test[index])][int(y_pred[index])]+=1
    #概率
    for i in range(len(target_names)):
        matrix[:,i]=matrix[:,i]/np.sum(matrix[:,i])

    plotCM(target_names, matrix, "")

def extract_features(model,x,y,sample_count):

    features=model.predict(x);
    labels=np.argmax(y,axis=1)
    return features,labels

def loadData(allX,allY):
    random.seed(0)
    index = list(range(len(allY)));
    random.shuffle(index)
    allX = allX[index, :]
    allY = allY[index, :]
    val = 0.8
    x_train, y_train = allX[0:int(len(allY) * val), :], allY[0:int(len(allY) * val), :]
    x_test, y_test = allX[int(len(allY) * val):, :], allY[int(len(allY) * val):, :]
    # print(x_train.shape)
    x_train = x_train.reshape(-1, n_step, n_input)
    x_test = x_test.reshape(-1, n_step, n_input)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    mean = np.mean(x_train)
    std = np.std(x_train)
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


weight_decay=0.005
learning_rate = 1e-4
training_iters = 1000
batch_size = 64
display_step = 10

n_input = 40
n_step = 40
n_hidden = 40
n_classes = 0
target_names=sorted(os.listdir('./raw_data'))
path="./data/pro1_data"
if __name__=="__main__":
    n_classes=len(os.listdir(path))
    # loaddata(path)
    allX = np.load(path + "/allX.npy")[:,:1600]
    allY = np.load(path + "/allY.npy")
    print(allX.shape)
    print(allY.shape)
    n_input = 40
    n_step = allX.shape[1] // n_input

    print("load data......")
    x_train, y_train, x_test, y_test = loadData(allX, allY)

    model=keras.models.load_model('best.hdf5')
    model.summary()

    # 已有的model在load权重过后
    # 取某一层的输出为输出新建为model，采用函数模型
    flatten_1 = Model(inputs=model.input,
                               outputs=model.get_layer('activation_1').output)

    print("load feature......")
    train_features,train_labels=extract_features(flatten_1,x_train,y_train,len(x_train))
    test_features, test_labels = extract_features(flatten_1,x_test,y_test, len(x_test))

    print(train_features.shape)
    print(train_labels.shape)
    print("train data......")
    clf = svm.SVC()  # class
    clf.fit(train_features, train_labels)  # training the svc model

    print("test data......")
    y_pred=clf.predict(test_features)
    y_pred_copy=clf.decision_function(test_features)

    Y_test=test_labels;
    print(classification_report(Y_test, y_pred, target_names=target_names))

    matrix = np.zeros((len(target_names), len(target_names)));
    for index in range(len(y_pred)):
        matrix[int(Y_test[index])][int(y_pred[index])] += 1

    plotCM(target_names, matrix, "")

    # # ROC
    # fpr, tpr, thresholds = roc_curve(Y_test, y_pred_copy)
    # roc_auc = auc(fpr, tpr)
    # lw = 2
    # plt.figure(figsize=(10, 10))
    # plt.plot(fpr, tpr, color='darkorange',
    #          lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)  ###假正率为横坐标，真正率为纵坐标做曲线
    # plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.05])
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('Receiver operating characteristic example')
    # plt.legend(loc="lower right")
    # plt.show()

