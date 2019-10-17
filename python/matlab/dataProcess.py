import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


def readCsv(path):
    df=pd.read_csv(path,header=None)
    # print(df)
    # pass
    data=df.values
    return data

def tmp():
    data = readCsv("D:\project\matlab\data\\31_.txt")
    plt.plot(data)
    plt.show()
    data = data[1050000:1350000, :]
    df = pd.DataFrame(data)
    df.to_csv("D:\project\matlab\data\\31__.txt", header=None, index=False)

    data = readCsv("D:\project\matlab\data\\31__.txt")

    plt.plot(data)
    plt.show()
if __name__=="__main__":
    # path='./data//整理后'
    # data=readCsv(num_file[20])
    # plt.plot(data)
    # plt.show()

    class_id = {'car': 0, 'ysgb': 1, 'gb': 2, 'ystk': 3, 'tk': 4}
    class_num = {'car': [7, 23], 'ysgb': [22, 24], 'gb': [25], 'ystk': [2, 3, 4, 5, 6, 20],
                 'tk': [21]}  # 8mm , 27, 28, 29, 30, 31
    num_file = {}

    for file in os.listdir('./data'):
        if len(file.split('_')) > 1:
            num_file[int(file.split('_')[0])] = os.path.join('./data', file)

    print(num_file)

    length=40000
    allData=np.zeros((1,length+1))
    for key in class_id:
        for num in class_num[key]:
            print(num)
            data=readCsv(num_file[num])
            # data=np.reshape(data,(-1,40000))
            # print(data.shape)
            for i in range(length,data.shape[0],1000):
                tmpdata=data[(int(i)-length):int(i)]
                tmpdata=np.reshape(tmpdata,(1,len(tmpdata)))
                label=np.zeros((1,1),dtype='int')
                label[0,0]=class_id[key]
                tmpdata=np.hstack((tmpdata,label))
                # print(tmpdata.shape)
                allData=np.vstack((allData,tmpdata))
    print(allData[:,-1])
    np.save('data8mm.npy',allData[1:,:])

    class_id = {'car': 0, 'ysgb': 1, 'gb': 2, 'ystk': 3, 'tk': 4}
    class_num={'car':[16],'ysgb':[13,14,15,17],'gb':[15],'ystk':[1,8,9,10,11,12],'tk':[13,14]}#3mm ,27,28,29,30,31
    num_file = {}

    for file in os.listdir('./data'):
        if len(file.split('_')) > 1:
            num_file[int(file.split('_')[0])] = os.path.join('./data', file)

    print(num_file)

    length = 40000
    allData = np.zeros((1, length + 1))
    for key in class_id:
        for num in class_num[key]:
            print(num)
            data = readCsv(num_file[num])
            # data=np.reshape(data,(-1,40000))
            # print(data.shape)
            for i in range(length, data.shape[0], 1000):
                tmpdata = data[(int(i) - length):int(i)]
                tmpdata = np.reshape(tmpdata, (1, len(tmpdata)))
                label = np.zeros((1, 1), dtype='int')
                label[0, 0] = class_id[key]
                tmpdata = np.hstack((tmpdata, label))
                # print(tmpdata.shape)
                allData = np.vstack((allData, tmpdata))
    print(allData[:, -1])
    np.save('data3mm.npy', allData[1:,:])


