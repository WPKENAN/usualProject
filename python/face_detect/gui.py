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

from train import *

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=400, height=10)
        self.pack()
        self.File="1.png"
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
        self.norm_size = norm_size
        self.labels_list = os.listdir("./images");
        self.labels_list.sort();
        print(self.labels_list)

        # load the trained convolutional neural network
        print("[INFO] loading network...")
        self.model = load_model("best.hdf5")
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
        # print (result.shape)
        proba = np.max(result)
        print(np.where(result == proba))
        number = np.where(result == proba)[0]

        print(number)
        print(self.labels_list[number[0]])

        return self.labels_list[number[0]],proba*100

    def processEvent(self, event):
        pass

        # function to be called when mouse is clicked
    def printcoords(self):
        try:
            self.File = filedialog.askopenfilename(parent=root, initialdir="./images", title='Choose an image.')
            self.path_label["text"]=self.File;
            label_name,val=self.predictWord()
            self.pilImage = Image.open(self.File).resize((993,516))
            self.tkImage = ImageTk.PhotoImage(image=self.pilImage);
            self.pre_label["text"]="这是:  {}    概率为:  {:.2f}% " .format(label_name,val)
            self.label["image"]=self.tkImage
        except:
            pass

if __name__ == '__main__':
    root = tk.Tk()
    root.title("人脸识别系统")
    app = App(root)
    root.mainloop()
