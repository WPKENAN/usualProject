from sklearn.metrics import classification_report
import numpy as np
from train import *
import keras
import os
from keras.applications.imagenet_utils import decode_predictions
from sklearn.metrics import roc_curve, auc
import  numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import copy
def plotCM(classes, matrix, savname):
    """classes: a list of class names"""

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(matrix)
    fig.colorbar(cax)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            ax.text(i, j, str('%.2f' % (matrix[i, j])), va='center', ha='center',fontsize=10,color='r')
    ax.set_xticklabels([''] + classes, rotation=90,fontsize=10)

    ax.set_yticklabels([''] + classes,fontsize=10)
    ax.set_xlabel('True')
    ax.set_ylabel('Predict')

    # save
    # plt.savefig(savname)
    plt.show()

def load_data(path):
    print(path)

    labels_list=os.listdir(path);
    labels_list.sort();
    print("[INFO] loading images...")
    data = []
    labels = []
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(paths.list_images(path)))
    # print(imagePaths)
    # dda
    random.seed(42)
    random.shuffle(imagePaths)
    # loop over the input images
    for imagePath in imagePaths:
        # load the image, pre-process it, and store it in the data list
        # print(imagePath)
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (norm_size, norm_size))
        image = img_to_array(image)
        data.append(image)

        # extract the class label from the image path and update the
        # labels list
        # print(imagePath.split(os.path.sep)[-2])
        label = labels_list.index(imagePath.split(os.path.sep)[-2])
        labels.append(label)

    # scale the raw pixel intensities to the range [0, 1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # convert the labels from integers to vectors
    labels = to_categorical(labels, num_classes=CLASS_NUM)
    return data, labels

if __name__=="__main__":
    all = "../images";
    val = "../val"
    CLASS_NUM = len(os.listdir(all))
    target_names=os.listdir(all)

    #x_test, Y_test = load_data(all)#全部图片
    x_test, Y_test = load_data(val)#验证集的图片

    model=keras.models.load_model("./best.hdf5")
    Y_test = np.argmax(Y_test, axis=1)  # Convert one-hot to index这里把onehot转成了整数[1,2,10,1,2,1]
    print(Y_test)
    y_pred = model.predict(x_test)  # 这里假设你的GT标注也是整数 [1,2,10,1,2,1]
    y_pred_copy=copy.deepcopy(y_pred)
    # print(y_pred)
    print(y_pred.shape)
    y_pred=np.argmax(y_pred, axis=1)

    print(classification_report(Y_test, y_pred,target_names=target_names))

    matrix = np.zeros((len(target_names), len(target_names)));
    for index in range(len(y_pred)):
        matrix[int(Y_test[index])][int(y_pred[index])] += 1

    plotCM(target_names, matrix, "")

    #ROC
    fpr, tpr, thresholds = roc_curve(Y_test, y_pred_copy[:,1])
    roc_auc = auc(fpr, tpr)
    lw = 2
    plt.figure(figsize=(10, 10))
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)  ###假正率为横坐标，真正率为纵坐标做曲线
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()