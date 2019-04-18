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

traindata = pd.read_csv('C:\\Users\Anzhi\Desktop\\Network-Intrusion-Detection-master\\UNSW-NB15\\UNSW_NB15_training-set.csv')
testdata = pd.read_csv('C:\\Users\Anzhi\Desktop\\Network-Intrusion-Detection-master\\UNSW-NB15.\\UNSW_NB15_testing-set.csv')
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


# try using different optimizers and different optimizer configs




from sklearn.metrics import confusion_matrix
import os
model.load_weights("kddresults/rnn/fullmodel/rnn_model.hdf5")
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])


y_pred = model.predict_classes(X_test)
y_test=np.transpose(np.array([y_test.tolist()]))
print(y_test.shape)
print(y_pred.shape)
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

'''
print(cm)
tp = cm[0][0]
fp = cm[0][1]
tn = cm[1][1]
fn = cm[1][0]
print("tp")
print(tp)
print("fp")
print(fp)
print("tn")
print(tn)
print("fn")
print(fn)

print("tpr")
tpr = float(tp)/(tp+fn)
print("fpr")
fpr = float(fp)/(fp+tn)
print("LSTM acc")
print(tpr)
print(fpr)


model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
loss, accuracy = model.evaluate(X_train, y_train1)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))

'''



'''
# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
checkpointer = callbacks.ModelCheckpoint(filepath="kddresults/lstm2layer/checkpoint-{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='val_acc',mode='max')
csv_logger = CSVLogger('training_set_iranalysis1.csv',separator=',', append=False)
model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=1000, validation_data=(X_test, y_test),callbacks=[checkpointer,csv_logger])
model.save("kddresults/lstm2layer/fullmodel/lstm2layer_model.hdf5")

loss, accuracy = model.evaluate(X_test, y_test)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
y_pred = model.predict_classes(X_test)
np.savetxt('kddresults/lstm2layer/lstm2predicted.txt', np.transpose([y_test,y_pred]), fmt='%01d')
'''






