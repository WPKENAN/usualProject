'''
Created on 2019年2月16日
    时间序列预测问题可以通过滑动窗口法转换为监督学习问题
@author: Administrator
'''
import random
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
    cityframe = read_csv('month_rate.csv', usecols=[1],
                         engine='python', skipfooter=0)
    dataframe = read_csv('month_rate.csv', usecols=[5],
                         engine='python', skipfooter=0)
    # dataframe = read_csv('D:\github\\usualProject\python\lstm\\test.csv', usecols=[1], engine='python', skipfooter=3)

    # city = input("please in put FZDBM: ");
    # city = city.upper();
    citys = cityframe.values;
    datasets = dataframe.values
    # 将整型变为float
    datasets = datasets.astype('float32')

    outfile = open("predict.csv", 'w');
    outfile.write("city,history,pre1,pre2,pre3,pre4,pre5\n")
    citys_set=set();
    for i in citys:
        # print(i[0])
        citys_set.add(i[0]);
    fff=0;
    for city in citys_set:
        # fff=fff+1
        # if fff>2:
        #     outfile.close()
        #     break;
        # city=city
        dataset = numpy.zeros((sum(citys == city)[0], 1))
        print("总共找到 {} 个历史数据".format(sum(citys == city)[0]))
        count = 0;
        for i in range(len(citys)):
            if citys[i] == city:
                dataset[count] = datasets[i]
                count = count + 1;
        print("{}城市历史收入:".format(city));
        print(dataset)
        dataset=dataset[::-1]
        print("开始预测")
        # 数据处理，归一化至0~1之间
        scaler = MinMaxScaler(feature_range=(0, 1))
        dataset = scaler.fit_transform(dataset)

        test_size = 10;
        dataset=numpy.vstack((dataset,numpy.zeros((test_size,1))))
        # 划分训练集和测试集
        train_size = int(len(dataset)-10)
        test_size = 10;


        if sum(citys == city)[0]==1:
            continue
        if sum(citys == city)[0] <3:
            look_back=1;
        elif sum(citys == city)[0] <15:
            look_back=2;
        else:
            look_back = min(12,sum(citys == city)[0])  # 往回看?月
        train, test = dataset[0:train_size, :], dataset[train_size-look_back:len(dataset), :]
        print(len(train),len(test))

        # 创建测试集和训练集
        # look_back = 1#往回看?天
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
            model.fit(trainX, trainY, batch_size=16, nb_epoch=32, callbacks=[checkpointer, csv_logger])
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


        print(numpy.average(train))
        if min(testPredict)<0:
            testPredict=testPredict-min(testPredict)+random.random();
        testPredictPlot = numpy.empty_like(dataset[0:10,:])
        testPredictPlot[:, :] = numpy.nan
        testPredictPlot[0:10, :] = testPredict

        print(numpy.shape(testPredict))

        # plt.plot(scaler.inverse_transform(dataset[0:len(dataset)-test_size]),label='realdata')
        # plt.title("history data")
        # plt.figure()
        # plt.plot(trainPredictPlot)
        # print(testY)
        # print(testPredict)
        # plt.plot(testY)
        print("predict income : ")
        print(testPredict)

        outfile.write("{},".format(city))
        # outfile.write("城市{}历史值,".format(city))
        for i in train:
            outfile.write("{}  ".format(i[0]))
        outfile.write(",")
        # outfile.write("预测值接下来10个月,")
        for i in testPredict[0:5,:]:
            outfile.write("{},".format(i[0]));
        outfile.write("\n")
        # plt.plot(testPredictPlot,label='predata'.format(len(testPredict)))
        # plt.title("city {} next {} months income-predict".format(city,10));
        # plt.legend();
        # plt.plot([823,823],[-20,20])
        # plt.grid()
        # plt.show();