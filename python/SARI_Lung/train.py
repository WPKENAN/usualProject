from model import *
import numpy as np
import keras
from keras.callbacks import ModelCheckpoint
import random
import os
import cv2 as cv
from imutils import paths
from keras.preprocessing.image import img_to_array
import matplotlib.pyplot as plt

norm_size=norm_size
def load_Train_data(imagefolder,labelfolder):
    print("[INFO] loading images...")
    imagedata = []
    labeldata = []
    # grab the image paths and randomly shuffle them
    imagePaths = os.listdir(imagefolder)

    random.seed(42)
    random.shuffle(imagePaths)
    # loop over the input images
    count=0
    for imagePath in imagePaths:
        count+=1
        print(count)
        # load the image, pre-process it, and store it in the data list
        # print(imagePath)
        image = cv.imread(os.path.join(imagefolder,imagePath))[:,:,0]
        image = cv.resize(image, (norm_size, norm_size))
        image = img_to_array(image)
        imagedata.append(image)

        label = cv.imread(os.path.join(labelfolder, imagePath))[:, :, 0]
        label = cv.resize(label, (norm_size, norm_size))
        label = img_to_array(label)
        labeldata.append(label)

    # scale the raw pixel intensities to the range [0, 1]

    imagedata = np.array(imagedata, dtype=np.float32)
    avg=np.average(imagedata);
    std=np.std(imagedata);
    out=open("config",'w')
    out.write('{},{}\n'.format(avg,std))
    out.close()
    print(avg,std)
    imagedata=(imagedata-avg)/std

    labeldata = np.array(labeldata, dtype=np.float32)
    labeldata[labeldata < 1] = 0;
    labeldata[labeldata >= 1] = 1;
    # labeldata[labeldata>1]=1;

    return imagedata,labeldata

if __name__=="__main__":
    train=1;

    trainX,trainY=load_Train_data(os.path.join("D:\github\Data\SARI",'Lung_png'),os.path.join('D:\github\Data\SARI','Lung_label'))
    print(trainX.shape)
    print(trainY.shape)
    print(np.sum(trainY==1))
    print(np.sum(trainY==0))
    print(np.sum(trainY==0)/(np.sum(trainY==0)+np.sum(trainY==1)))
    # da

    # cv.imshow("main",trainY[1,:,:,0])
    # cv.waitKey(3000)

    if train:
        EPOCHS=50
        model = unet()
        model.summary()
        # model=keras.models.load_model("best.hdf5",custom_objects={'bce_dice_loss': bce_dice_loss})
        model_checkpoint = ModelCheckpoint('best.hdf5', monitor='val_acc',verbose=1, save_best_only=True)
        tb_cb = keras.callbacks.TensorBoard(log_dir="./log", write_images=1, histogram_freq=0)

        H=model.fit(trainX,trainY,batch_size=4,epochs=EPOCHS,validation_split=0.1,callbacks=[model_checkpoint,tb_cb])
        model.save("./lasted.hdf5")

        plt.style.use("ggplot")
        plt.figure()
        N = EPOCHS
        plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
        plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
        plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
        plt.title("Training Loss and Accuracy on foot classifier")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="lower left")
        plt.savefig("train.png")

    else:
        model=keras.models.load_model("best.hdf5",custom_objects={'bce_dice_loss': bce_dice_loss})
        scores = model.evaluate(trainX, trainY, verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

        img=np.round(model.predict(trainX[0:1,:,:,0:1]))
        img=img.astype(np.uint8)
        print(np.sum(img>0))
        img[img>0]=255
        cv.imshow("mian",img[0,:,:,0])
        cv.waitKey(5000)
