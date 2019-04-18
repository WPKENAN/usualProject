import numpy as np

np.random.seed(1337)

from keras.models import Sequential

from keras.layers import Dense

import matplotlib.pyplot as plt



# 生成数据

X = np.linspace(-1, 1, 200)  # 在返回（-1, 1）范围内的等差序列

np.random.shuffle(X)  # 打乱顺序

Y = 0.5 * X + 2 + np.random.normal(0, 0.05, (200,))  # 生成Y并添加噪声

# X, Y = f_t_t_read.data_get()


# plot

plt.scatter(X, Y)

plt.show()

X_train, Y_train = X[:160], Y[:160]  # 前160组数据为训练数据集

X_test, Y_test = X[160:], Y[160:]  # 后40组数据为测试数据集

# 构建神经网络模型

model = Sequential()

# model.add(Dense(units=1,input_dim=1))

model.add(Dense(units=1, input_shape=(1,)))

# `Dense` implements the operation:

# `output = activation(dot(input, kernel) + bias)`

##


##以下三种方法等价

##model = Sequential()

##方法（1）model.add(LSTM(32, input_shape=(10, 64)))

##方法（2）model.add(LSTM(32, batch_input_shape=(None, 10, 64)))

##方法（3）model.add(LSTM(32, input_length=10, input_dim=64))

##有些2D层，如Dense，支持通过指定输入维度input_dim来隐含的指定输入数据的shape，

##一些3D层，的时域（时空）层，支持通过参数input_dim和input_length来指定输入数据的shape

# input_dim, input_length = input_shape(input_length, input_dim)

# input_dim               = input_shape(input_dim,)


##model.add(Dense(32, input_shape=(16,)))

## |      # now the model will take as input arrays of shape (*, 16)

## |      # and output arrays of shape (*, 32)


# 选定loss函数和优化器

model.compile(loss='mse', optimizer='sgd')

# 训练过程

print('Training -----------')

for step in range(501):

    cost = model.train_on_batch(X_train, Y_train)

    print('model.output_shape:', model.output_shape)

    if step % 50 == 0:
        print("After %d trainings, the cost: %f" % (step, cost))

    # 测试过程

print('\nTesting ------------')

cost = model.evaluate(X_test, Y_test, batch_size=40)

print('test cost:', cost)

W, b = model.layers[0].get_weights()

print('Weights=', W, '\nbiases=', b)

# 将训练结果绘出

Y_pred = model.predict(X_test)

plt.scatter(X_test, Y_test)

plt.plot(X_test, Y_pred)

plt.show()

# ---------------------------------以上参考，以下可用------------------------------------------

import numpy

import pandas

from keras.models import Sequential

from keras.layers import Dense

from keras.wrappers.scikit_learn import KerasRegressor

from sklearn.model_selection import cross_val_score

from sklearn.model_selection import KFold

from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline

from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt


def data_get():
    forecast_day = '024'

    single_grid_id = 2439  # lon = 117.5, lat = 40, beijing

    df = pandas.read_csv(forecast_day + '_' + str(single_grid_id) + '.csv', index_col=0, encoding='gbk')

    df[df > 9000] = numpy.nan

    df = df.dropna(how='any')

    dataset = df.values

    X = dataset[:, 0:-1]

    Y = dataset[:, -1]

    return (X, Y)


# define base mode

def baseline_model():
    # create model

    model = Sequential()

    model.add(Dense(20, input_dim=X.shape[1], kernel_initializer='normal', activation='relu'))

    model.add(Dense(20, activation='relu'))

    model.add(Dense(1, kernel_initializer='normal'))

    # Compile model

    model.compile(loss='mean_squared_error', optimizer='adam')

    return (model)


def function_rmse(v):
    rmse = []

    for i in v:
        rmse.append(i * i)

    rmse = numpy.sqrt(sum(rmse) / len(v))

    return (rmse)


# load dataset

##dataframe = pandas.read_csv("housing.csv", delim_whitespace=True, header=None)

##dataset = dataframe.values

# split into input (X) and output (Y) variables

##X = dataset[:, 0:13]

##Y = dataset[:, 13]


X, Y = data_get()

# split into train and test groups

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.99, random_state=42)

model = baseline_model()

# 训练过程

print('Training -----------')

for step in range(501):

    cost = model.train_on_batch(X_train, Y_train)

    # print('model.output_shape:',model.output_shape)

    if step % 50 == 0:
        print("After %d trainings, the cost: %f" % (step, cost))

    # 测试过程

print('\nTesting ------------')

cost = model.evaluate(X_test, Y_test, batch_size=40)

print('test cost:', cost)

W, b = model.layers[0].get_weights()

# print('Weights=', W, '\nbiases=', b)


# 将训练结果绘出

Y_pred = model.predict(X)

Y_pred = Y_pred.reshape(len(Y_pred))

# Y_ensemble = X.mean(1)

Y_ensemble = X[:, 0]

Y1 = Y_ensemble - Y

Y2 = Y_pred - Y

##

plt.plot(Y1, 'b')

plt.plot(Y2, 'r')

##plt.plot(Y,'k')

##plt.plot(Y_ensemble,'b')

##plt.plot(Y_pred,'r')

###plt.xlim([100,200])

plt.show(block=False)

print(function_rmse(Y1))

print(function_rmse(Y2))

# print(aaa)

plt.scatter(Y_test, Y_pred)

Y_ensemble = X.mean(1)

plt.scatter(Y_test, Y_ensemble, 'r')

# plt.plot(Y_pred)

plt.show()

# print(aaa)