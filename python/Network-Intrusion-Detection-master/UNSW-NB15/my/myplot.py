from __future__ import division
import  numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def readCsv(path):
    result={}
    contents=open(path).readlines();
    for i in range(len(contents)):
        contents[i]=contents[i].strip('\n').split(',');
        result[contents[i][0]]=[]

        for j in range(1,len(contents[i])):
            if contents[i][j]=='':
                continue
            contents[i][j]=float(contents[i][j]);
            result[contents[i][0]].append(contents[i][j])
    print(result)
    return result

def plotCM(classes, matrix, savname):
    """classes: a list of class names"""
    # Normalize by row
    # matrix = matrix.astype(np.float)
    # linesum = matrix.sum(1)
    # linesum = np.dot(linesum.reshape(-1, 1), np.ones((1, matrix.shape[1])))
    # matrix /= linesum
    # plot
    plt.switch_backend('agg')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(matrix)
    fig.colorbar(cax)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            ax.text(i, j, str('%.2f' % (matrix[i, j])), va='center', ha='center')
    ax.set_xticklabels([''] + classes, rotation=90)
    ax.set_yticklabels([''] + classes)
    # save
    plt.savefig(savname)

if __name__=="__main__":
    # print("hello")
    cnnPath="./cnn/result.csv"
    rnnPath = "./rnn/result.csv"
    knnPath = "./knn/result.csv"
    cnnResult=readCsv(cnnPath)
    rnnResult=readCsv(rnnPath)
    knnResult=readCsv(knnPath)

    name_list=['CNN','RNN','KNN']
    plt.figure()
    plt.subplot(221)
    plt.bar(range(3),[cnnResult['accuracy'][0],rnnResult['accuracy'][0],knnResult['accuracy'][0]],color='rgb',tick_label=name_list);
    plt.title('accuracy')
    # plt.show()


    plt.subplot(222)
    plt.bar(range(3), [cnnResult['recall'][0], rnnResult['recall'][0], knnResult['recall'][0]], color='rgb',tick_label=name_list);
    plt.title('recall')
    # plt.show()


    plt.subplot(223)
    plt.bar(range(3), [cnnResult['f1score'][0], rnnResult['f1score'][0], knnResult['f1score'][0]], color='rgb',
            tick_label=name_list);
    plt.title('f1score')
    # plt.show()


    plt.subplot(224)
    plt.bar(range(3), [cnnResult['precision'][0], rnnResult['precision'][0], knnResult['precision'][0]], color='rgb',
            tick_label=name_list);
    plt.title('precision')
    plt.savefig('result.png')
    plt.show()

    #混淆矩阵M的每一行代表每个真实类（GT），每一列表示预测的类,Mij表示GroundTruth类别为i的所有数据中被预测为类别j的数目。
    print(np.array(rnnResult['confusion_matrix']).reshape(2,2))
    plotCM(['normal','un_normal'],np.array(cnnResult['confusion_matrix']).reshape(2,2),'CNN_confusion_matrix')
    plotCM(['normal', 'un_normal'], np.array(rnnResult['confusion_matrix']).reshape(2, 2), 'RNN_confusion_matrix')
    plotCM(['normal', 'un_normal'], np.array(knnResult['confusion_matrix']).reshape(2, 2), 'KNN_confusion_matrix')








