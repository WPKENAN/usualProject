from __future__ import print_function
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb
from keras.utils.np_utils import to_categorical
from sklearn.metrics import (precision_score, recall_score,
                             f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger

traindata = pd.read_csv('..\\UNSW_NB15_training-set.csv')
testdata = pd.read_csv('..\\UNSW_NB15_testing-set.csv')
traindata = pd.get_dummies(data=traindata, columns=['proto', 'service', 'state'])
testdata = pd.get_dummies(data=testdata, columns=['proto', 'service', 'state'])

X = traindata.iloc[:,1:191]
Y = traindata.iloc[:,0]
C = testdata.iloc[:,0]
T = testdata.iloc[:,1:191]

scaler = Normalizer().fit(X)
trainX = scaler.transform(X)

scaler = Normalizer().fit(T)
testT = scaler.transform(T)

y_train = np.array(Y)
y_test = np.array(C)


# reshape input to be [samples, time steps, features]
X_train = np.reshape(trainX, (trainX.shape[0],1,trainX.shape[1]))
X_test = np.reshape(testT, (testT.shape[0],1,testT.shape[1]))


rnn_output_size = 128
# 1. define the network
model = Sequential()
model.add(SimpleRNN(32,input_dim=190, return_sequences=True))  # try using a GRU instead, for fun
model.add(Dropout(0.1))
model.add(SimpleRNN(32, return_sequences=True))  # try using a GRU instead, for fun
model.add(Dropout(0.1))
model.add(SimpleRNN(32, return_sequences=True))  # try using a GRU instead, for fun
model.add(Dropout(0.1))
model.add(SimpleRNN(32, return_sequences=False))  # try using a GRU instead, for fun
model.add(Dropout(0.1))
model.add(Dense(1))
model.add(Activation('sigmoid'))

# cnn=load_model('results/cnn1results/rnn_model.hdf5')
# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
checkpointer = callbacks.ModelCheckpoint(filepath="checkpoint.hdf5", verbose=1, save_best_only=True, monitor='val_acc',mode='max')
csv_logger = CSVLogger('training_set_iranalysis1.csv',separator=',', append=False)
model.fit(X_train, y_train, batch_size=256, nb_epoch=20, validation_data=(X_test, y_test),callbacks=[checkpointer,csv_logger])
model.save("rnn_model.hdf5")

loss, accuracy = model.evaluate(X_test, y_test)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
y_pred = model.predict_classes(X_test)

np.savetxt('rnnpredicted.txt', np.transpose(np.array([y_test.tolist(),y_pred.reshape(len(y_pred)).tolist()])), fmt='%01d')







