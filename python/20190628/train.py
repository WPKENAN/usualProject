from keras.layers import Embedding,Bidirectional,Input,concatenate,BatchNormalization,Dropout,Dense,LSTM
from keras.models import Model
import keras.backend as K
import pandas as pd
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import keras
from keras.callbacks import TensorBoard
from keras.callbacks import ModelCheckpoint

import random
APP=100
def readCsv(path):
    df=pd.read_csv(path,header=None)
    # print(df)
    data=df.values
    query_id,query_title_id,label = data[:, 0],data[:, 2],data[:, 4]

    query=[]
    title = []
    labels=[]
    for i in range(len(data[:, 1])):
        if label[i]==0 and random.random()<0.3175 or label[i]==1:
            query.append([])
            title.append([])
            for j in data[i, 1].split(' '):
                query[-1].append(int(j)%APP)
            for j in data[i, 3].split(' '):
                title[-1].append(int(j)%APP)
            labels.append(label[i])


    return query_id,query,query_title_id,title,np.array(labels)

def SiameseBiLSTM(vocab, max_length):
    # K.clear_session()
    embedding = Embedding(input_dim=vocab, output_dim=100, input_length=max_length)
    bilstm = Bidirectional(LSTM(64,kernel_regularizer=keras.regularizers.l2(0.05)))

    sequence_input1 = Input(shape=(max_length,))
    embedded_sequences_1 = embedding(sequence_input1)
    x1 = bilstm(embedded_sequences_1)

    sequence_input2 = Input(shape=(max_length,))
    embedded_sequences_2 = embedding(sequence_input2)
    x2 = bilstm(embedded_sequences_2)

    merged = concatenate([x1, x2])
    merged = BatchNormalization()(merged)
    merged = Dropout(0.5)(merged)
    merged = Dense(50, activation="relu",kernel_regularizer=keras.regularizers.l2(0.05))(merged)
    merged = BatchNormalization()(merged)
    merged = Dropout(0.5)(merged)
    preds = Dense(1, activation='sigmoid')(merged)
    model = Model(inputs=[sequence_input1, sequence_input2], outputs=preds)
    return model

if __name__=="__main__":
    path="data.csv"
    query_id, query, query_title_id, title, label=readCsv(path)
    maxLength=35
    Sens_1 = pad_sequences(query, maxlen=maxLength)
    Sens_2 = pad_sequences(title, maxlen=maxLength)
    print(np.sum(label)/len(label))

    model = SiameseBiLSTM(APP, maxLength)
    adam = keras.optimizers.Adam(lr=0.0005)
    model.compile(loss='binary_crossentropy', optimizer=adam,metrics=['accuracy'])
    model.summary()
    model_checkpoint = ModelCheckpoint('best.hdf5', monitor='val_acc', verbose=1, save_best_only=True)
    tb_cb = keras.callbacks.TensorBoard(log_dir="./log", write_images=1, histogram_freq=0)

    model.fit([Sens_1,Sens_2],label,batch_size=512,epochs=1000,validation_split=0.2,callbacks = [model_checkpoint, tb_cb])


    model=keras.models.load_model("best.hdf5")
    result=model.predict([Sens_1,Sens_2],batch_size=1024,verbose=1)
    result=np.round(result+0.1)

    scale = len(result);
    threshold = 0.5
    arr = []
    random.seed(0)
    for i in range(scale):
        if random.random() > threshold:
            arr.append(1);
        else:
            arr.append(0)
    arr = np.array(arr)

    count=0;
    for i in range(scale):
        if label[i] == result[i,0]:
            count += 1;
    print(count / scale)

    # print(np.round(result))