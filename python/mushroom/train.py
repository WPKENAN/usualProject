import pandas


import os
import pandas
import numpy as np
import random
import struct
np.random.seed(0)

from keras.datasets import mnist
from keras.models import Model
from keras.layers import Dense,Input
from keras.utils.np_utils import to_categorical
import matplotlib.pyplot as plt
from keras import regularizers
import keras


class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch': [], 'epoch': []}
        self.accuracy = {'batch': [], 'epoch': []}
        self.val_loss = {'batch': [], 'epoch': []}
        self.val_acc = {'batch': [], 'epoch': []}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))

    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        #创建一个图
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')#plt.plot(x,y)，这个将数据画成曲线
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_acc
            plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')

        plt.grid(True)#设置网格形式
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')#给x，y轴加注释
        plt.legend(loc="upper right")#设置图例显示位置
        plt.savefig('result.png')
        plt.show()


def readdata():
    data=pandas.read_csv("data.csv",header=None);
    # data=data.iloc[0:2000,:]
    y=data.iloc[:,0].values;
    y=y-1;
    print(y)
    x=pandas.get_dummies(data.astype(str).iloc[:,[3,5,6,20,22]]).values
    # x = data.astype(str).iloc[:, 1:23].values
    index=[]
    count=0;
    for i in range(sum(y)):
        if sum(y)>len(y)/2:
            if y[i]==0:
                index.append(i)
            if y[i]==1 and count<len(y)-sum(y) and random.random()<sum(y)/len(y):
                index.append(i);
                count=count+1;

        elif sum(y)<len(y)/2:
            if y[i]==1:
                index.append(i)
            if y[i]==0 and count<len(y)-sum(y) and random.random()<1-sum(y)/len(y):
                index.append(i);
                count=count+1;

    x=x[index,:]
    y=y[index]
    print(sum(y))
    print(y.shape)
    return x,y

def train():
    x, y = readdata()
    X_train = x
    y_train = y
    X_test = X_train.copy()
    y_test = y_train.copy()
    y_train_cate = to_categorical(y_train, num_classes=2)
    y_test_cate = to_categorical(y_test, num_classes=2)
    # print(y_test_cate)

    # 数据预处理
    X_train = X_train.astype('float32')  # minmax_normalized(归一化在（-0.5,0.5）)之间
    X_test = X_test.astype('float32')  # minmax_normalized
    X_train_len = X_train.shape[0]
    X_test_len = X_test.shape[0]

    X_train = X_train.reshape((X_train_len, -1))
    X_test = X_test.reshape((X_test_len, -1))

    print(X_train.shape)
    print(y_test.shape)
    # print(X_train.shape[1])
    history = LossHistory()

    input_img=Input(shape=(X_train.shape[1],))
    out=Dense(2,name='LR',activation='relu',activity_regularizer=regularizers.l1(0.01))(input_img)
    # out=Dense(2,activation='relu',activity_regularizer=regularizers.l1(0.01))(out)
    # out=Dense(100,activation='relu',activity_regularizer=regularizers.l1(0.01))(out)
    # out=Dense(100,activation='relu',activity_regularizer=regularizers.l1(0.01))(out)
    # out=Dense(50,activation='relu',activity_regularizer=regularizers.l1(0.01))(out)
    out=Dense(2,activation='softmax')(out)
    encoder=Model(inputs=input_img,outputs=out)
    encoder.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    encoder.fit(X_train,y_train_cate,epochs=10,batch_size=8,validation_split=0.3,shuffle=True,callbacks=[history],class_weight={0:1,1:1})
    #score=encoder.evaluate(X_test,y_test)
    #print(score)
    print(encoder.summary())
    # history.loss_plot('epoch')


    encoder.save('DNN.model')
    score=encoder.evaluate(X_test,y_test_cate)
    print("loss:{} acc:{}".format(score[0],score[1]))
    # print(score)
    history.loss_plot('epoch')

def predict():
    encoder=keras.models.load_model('DNN.model')
    #预测开始
    data=pandas.read_csv("data.csv",header=None);
    y=data.iloc[:,0].values;
    y=y-1;
    print(y.reshape(len(y),-1))
    x=pandas.get_dummies(data.astype(str).iloc[:,[3,5,6,20,22]]).values
    # x = data.astype(str).iloc[:, 1:23].values
    print(encoder.predict(x))
    # print(sum(y)/len(y))


if __name__=="__main__":
    t=0;
    if t==0:
        predict()
    elif t==1:
        train()