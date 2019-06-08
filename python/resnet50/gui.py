#encoding=utf-8
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import os

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
import matplotlib.pyplot as plt
# import  matplotlib
# matplotlib.use("Agg")
# import numpy as np
# import argparse
import random
import cv2
import os
import keras
import sys


# coding=utf-8
from keras.models import Model
from keras.layers import Input, Dense, BatchNormalization, Conv2D, MaxPooling2D, AveragePooling2D, ZeroPadding2D
from keras.layers import add, Flatten
# from keras.layers.convolutional import Conv2D,MaxPooling2D,AveragePooling2D
from keras.optimizers import SGD
import numpy as np
from keras.callbacks import ModelCheckpoint
import train
class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=400, height=10)
        self.pack()
        self.File="1.jpg"
        self.pilImage = Image.open(self.File).resize((993,516))
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.path_label = tk.Label(self, text=self.File, width=100)
        self.path_label.pack()
        self.label = tk.Label(self, image=self.tkImage,width=993,height=516)
        self.label.pack()
        self.button=tk.Button(root, text='choose an image', command=self.printcoords,width=20).pack()
        self.pre_label=tk.Label(self,text='这是:         概率为:        ',width=100)
        self.pre_label.pack()


        ############################################################################################准备模型阶段,提高效率
        self.norm_size = 128
        self.labels_list = os.listdir("./images");
        self.labels_list.sort();
        print(self.labels_list)

        # load the trained convolutional neural network
        print("[INFO] loading network...")
        self.model = load_model("ResNet50.hdf5")
        ################################################################################################
    def predictWord(self):
        image = cv2.imread(self.File)
        orig = image.copy()
        # pre-process the image for classification
        image = cv2.resize(image, (self.norm_size, self.norm_size))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        # classify the input image
        result = self.model.predict(image)[0]

        top5=[]
        for i in range(len(self.labels_list)):
            print(i)
            top5.append([result[i]*100,self.labels_list[i]])

        top5.sort(reverse=True)

        print(top5)
        return top5

    def processEvent(self, event):
        pass

        # function to be called when mouse is clicked
    def printcoords(self):
        try:
            self.File = filedialog.askopenfilename(parent=root, initialdir="./images", title='Choose an image.')
            self.path_label["text"]=self.File;
            top5=self.predictWord()
            print(top5[0][0],top5[0][1],top5[1][0],top5[1][1],top5[2][0],top5[2][1],top5[3][0],top5[3][1],top5[4][0],top5[4][1])
            self.pilImage = Image.open(self.File).resize((993,516))
            self.tkImage = ImageTk.PhotoImage(image=self.pilImage);
            self.pre_label["text"]="TOP5:  {}-{:.2f}%; {}-{:.2f}%; {}-{:.2f}%; {}-{:.2f}%; {}-{:.2f}% ".format(top5[0][1],top5[0][0],top5[1][1],top5[1][0],top5[2][1],top5[2][0],top5[3][1],top5[3][0],top5[4][1],top5[4][0])
            self.label["image"]=self.tkImage
        except:
            pass

if __name__ == '__main__':
    root = tk.Tk()
    root.title("足迹分类系统")
    app = App(root)
    root.mainloop()
