# coding: utf-8
#预测7月份北京的每日最高温
import xlrd
import xlwt
import os
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from numpy import newaxis
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
#变量声明
day_high = []  #一天中的最高温度
day_low = []    #一天中的最低温度
predict_series = []
result = []
day_new = []
out_put = []

#加载数据
def load_data(xls_file):
    data = xlrd.open_workbook(xls_file)
    for index in data.sheets():
        table = data.sheet_by_name(index.name)#通过名称获取
        nrows = table.nrows  #获取当前列表的行数
    for row in range(nrows):
        if (row != 0):
            day_high.append(table.row_values(row)[1]) #一天中的最高温度
            day_low.append(table.row_values(row)[2])  #一天中的最低温度

#数据预处理
def data_preprocess(data0):
    data = data0
#data.append(data[-1])
#print(data[-1])
    sequence_length = 20
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])  #得到长度为sequence_length 的向量，最后一个作为label
    result = np.array(result)

    row = round(0.9 * result.shape[0])
    train = result[:row, :]
    #print("train:",train)
    np.random.shuffle(train)
    x_train = train[:, :-1]
    #print(x_train)
    y_train = train[:, -1]
    x_test = result[row:, :-1]
    y_test = result[row:, -1]
    #print(x_test)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    return [x_train, y_train, x_test, y_test]

#构建LSTM模型
def build_model(layers):  #layers [1,50,100,1]
    model = Sequential()
    #Stack LSTM
    model.add(LSTM(input_dim=layers[0],output_dim=layers[1],return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(layers[2],return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim=layers[3]))
    model.add(Activation("linear"))
    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop")
    print("Compilation Time : ", time.time() - start)
    return model

#直接预测
def predict_point_by_point(model, data):
    predicted = model.predict(data)
    print('predicted shape:',np.array(predicted).shape)  #(412L,1L)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted

#画图
def plot_results(predicted_data, true_data, filename):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()
#plt.savefig(filename+'.png')

#list解嵌套
def nested_list(list_raw,result):
    for item in list_raw:
        if isinstance(item, list):
            nested_list(item,result)
        else:
            result.append(item)
    return  result

#main
load_data("北京.xls")    #加载数据
model = build_model([1,50,100,1])  #构建模型
day_new = day_high
for i in range(31):
    X_train, y_train, X_test, y_test = data_preprocess(day_new)
    model.fit(X_train,y_train,batch_size=512,nb_epoch=150,validation_split=0.05)
    point_by_point_predictions = predict_point_by_point(model, X_test)
    #print(point_by_point_predictions)
    result = nested_list(point_by_point_predictions,result)
    predict_series.append(round(result[-1],0))
    print(predict_series)
    day_new.append(round(result[-1],0))
    print(len(day_new))
    #print(day_new)
    print(predict_series)    #预测出的7月份连续31天的每日最高温