import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, LSTM, TimeDistributed, RepeatVector
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt

def readTrain():
  train = pd.read_csv("SPY.csv")
  return train

def augFeatures(train):
  train["Date"] = pd.to_datetime(train["Date"])
  train["year"] = train["Date"].dt.year
  train["month"] = train["Date"].dt.month
  train["date"] = train["Date"].dt.day
  train["day"] = train["Date"].dt.dayofweek
  return train

def shuffle(X,Y):
  np.random.seed(10)
  randomList = np.arange(X.shape[0])
  np.random.shuffle(randomList)
  return X[randomList], Y[randomList]

def normalize(train):
  train = train.drop(["Date"], axis=1)
  train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
  return train_norm

def buildTrain(train, pastDay=30, futureDay=5):
  X_train, Y_train = [], []
  for i in range(train.shape[0]-futureDay-pastDay):
    X_train.append(np.array(train.iloc[i:i+pastDay]))
    Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["Adj Close"]))
  return np.array(X_train), np.array(Y_train)

def splitData(X,Y,rate):
  X_train = X[int(X.shape[0]*rate):]
  Y_train = Y[int(Y.shape[0]*rate):]
  X_val = X[:int(X.shape[0]*rate)]
  Y_val = Y[:int(Y.shape[0]*rate)]
  return X_train, Y_train, X_val, Y_val

def buildOneToOneModel(shape):
  model = Sequential()
  model.add(LSTM(10, input_length=shape[1], input_dim=shape[2],return_sequences=True))
  # output shape: (1, 1)
  model.add(TimeDistributed(Dense(1)))    # or use model.add(Dense(1))
  model.compile(loss="mse", optimizer="adam")
  model.summary()
  return model


if __name__=="__main__":
    # read SPY.csv
    train = readTrain()

    # Augment the features (year, month, date, day)
    train_Aug = augFeatures(train)

    # Normalization
    train_norm = normalize(train_Aug)

    # build Data, use last 30 days to predict next 5 days
    X_train, Y_train = buildTrain(train_norm, 30, 5)

    # shuffle the data, and random seed is 10
    X_train, Y_train = shuffle(X_train, Y_train)

    # split training data and validation data
    X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)
    # X_trian: (5710, 30, 10)
    # Y_train: (5710, 5, 1)
    # X_val: (634, 30, 10)
    # Y_val: (634, 5, 1)

    train = readTrain()
    train_Aug = augFeatures(train)
    train_norm = normalize(train_Aug)
    # change the last day and next day
    X_train, Y_train = buildTrain(train_norm, 1, 1)
    X_train, Y_train = shuffle(X_train, Y_train)
    X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)

    # from 2 dimmension to 3 dimension
    Y_train = Y_train[:, np.newaxis]
    Y_val = Y_val[:, np.newaxis]

    model = buildOneToOneModel(X_train.shape)
    callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto")
    model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_val, Y_val), callbacks=[callback])



