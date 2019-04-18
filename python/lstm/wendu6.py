'''
Created on 2019年2月16日
    时间序列预测问题可以通过滑动窗口法转换为监督学习问题
@author: Administrator
'''

import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.utils.vis_utils import plot_model
from keras.layers.core import Dense, Activation, Dropout
from keras import callbacks
from keras.layers import LSTM, GRU, SimpleRNN
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger


# 创建数据集
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])

    return numpy.array(dataX), numpy.array(dataY)


if __name__ == '__main__':
    # 加载数据
    dataframe = read_csv('D:\github\\usualProject\python\lstm\\raw.csv', usecols=[7], engine='python', skipfooter=42500)
    # dataframe = read_csv('D:\github\\usualProject\python\lstm\\test.csv', usecols=[1], engine='python', skipfooter=3)
    dataset = dataframe.values
    # 将整型变为float
    dataset = dataset.astype('float32')

    print(numpy.shape(dataset))

    # 数据处理，归一化至0~1之间
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)

    # 划分训练集和测试集
    train_size = int(len(dataset) * 0.8)
    test_size = len(dataset) - train_size

    train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]
    print(len(train),len(test))

    # 创建测试集和训练集
    look_back = 3#往回看?天
    trainX, trainY = create_dataset(train, look_back)  # 单步预测
    testX, testY = create_dataset(test, look_back)
    print([numpy.shape(trainX),numpy.shape(testX)])

    print("训练样本数量{}".format(trainX.shape[0]))
    # 调整输入数据的格式
    trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1],1))  # （样本个数，1，输入的维度）
    testX = numpy.reshape(testX, (testX.shape[0], testX.shape[1],1))

    model = Sequential()
    layers=[1, 50, 100, 1]
    model.add(LSTM(input_dim=layers[0], output_dim=layers[1], return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(layers[2], return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim=layers[3]))
    model.add(Activation("linear"))

    #如果是测试模型则is_train=0,训练模型is_train=1
    is_train=1;
    if is_train==0:
        #加载模型
        model.load_weights("result/lstm_model.hdf5")
    else:
        # 加载模型
        model.load_weights("result/lstm_model.hdf5")
        model.compile(loss='mean_squared_error', optimizer='adam')
        checkpointer = callbacks.ModelCheckpoint(filepath="result/checkpoint-{epoch:02d}.hdf5", verbose=1,
                                                 save_best_only=True, monitor='val_loss', mode='auto')
        csv_logger = CSVLogger('result/lstm_train_analysis1.csv', separator=',', append=False)
        model.fit(trainX, trainY, batch_size=32, nb_epoch=64, callbacks=[checkpointer, csv_logger])
        model.save("result/lstm_model.hdf5")
        # 绘制网络结构
        plot_model(model, to_file='model.png', show_shapes=True);

    # 预测
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)



    # 反归一化
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])

    # 计算得分
    trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
    print('Test Score: %.2f RMSE' % (testScore))

    # 绘图
    trainPredictPlot = numpy.empty_like(dataset)
    trainPredictPlot[:, :] = numpy.nan
    trainPredictPlot[look_back:train_size, :] = trainPredict
    print(numpy.shape(trainPredict))

    testPredictPlot = numpy.empty_like(dataset)
    testPredictPlot[:, :] = numpy.nan
    testPredictPlot[train_size+look_back:len(dataset), :] = testPredict
    print(numpy.shape(testPredict))

    plt.plot(scaler.inverse_transform(dataset),label='realdata')
    # plt.plot(trainPredictPlot)
    # print(testY)
    # print(testPredict)
    # plt.plot(testY)
    plt.plot(testPredictPlot,label='last {} testPredictPlot'.format(len(testPredict)))
    plt.legend();
    # plt.plot([823,823],[-20,20])
    plt.grid()
    plt.show();