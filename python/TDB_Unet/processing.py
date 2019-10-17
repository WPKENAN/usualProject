import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import dicom
import os
import pydicom
import shutil
import random

def dcmTopng(dcmPath,pngPath):

    try:
        print(dcmPath,pngPath)
        dcm = pydicom.read_file(dcmPath)
        img = dcm.pixel_array
        print(np.min(img),np.max(img))
        img[img < 1000] = 0
        img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
        img = img.astype(np.uint8)
        equ = cv.equalizeHist(img)
        cv.imwrite(pngPath, equ)
    except:
        dcm = dicom.read_file(dcmPath)
        img = dcm.pixel_array
        # print(np.min(img))
        img[img < 980] = 0
        img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
        img = img.astype(np.uint8)
        equ = cv.equalizeHist(img)
        cv.imwrite(pngPath,equ)

def readFolder(path,outpath,labelPath):
    for i in os.listdir(path):
        for j in os.listdir(os.path.join(path,i)):
            for k in os.listdir(os.path.join(path,i,j)):
                if "dcm" in k:
                    continue
                    print(os.path.join(path,i,j))
                    dcmTopng(os.path.join(path,i,j,k),os.path.join(outpath,"{}_{}_{}.png".format(i,j,k.split('.')[0])))
                if "mask" in k:
                    print(os.path.join(path, i, j))
                    shutil.copy(os.path.join(path,i,j,k),os.path.join(labelPath,"{}_{}_{}".format(i,j,k.replace('_mask',''))))


def splitToImageLabel(path):
    if not os.path.exists(os.path.join(path,"balanceimage")):
        os.mkdir(os.path.join(path,"balanceimage"))
    else:
        shutil.rmtree(os.path.join(path,"balanceimage"))
        os.mkdir(os.path.join(path, "balanceimage"))

    if not os.path.exists(os.path.join(path,"balancelabel")):
        os.mkdir(os.path.join(path,"balancelabel"))
    else:
        shutil.rmtree(os.path.join(path,"balancelabel"))
        os.mkdir(os.path.join(path, "balancelabel"))

    count=0;
    a=[]
    for file in os.listdir(os.path.join(path,'labels')):
        img=cv.imread(os.path.join(path,'labels',file))[:,:,0]
        if np.sum(img>=1)/np.sum(img>-1) > 0.015:
            shutil.copy(os.path.join(path,'labels',file),os.path.join(path,'balancelabel',file))
            shutil.copy(os.path.join(path, 'images', file), os.path.join(path, 'balanceimage', file))
            count = count + 1
            print(count)
        if np.sum(img>=1)/np.sum(img>-1) == 0:
            if random.random() <0.0015:
                shutil.copy(os.path.join(path,'labels',file),os.path.join(path,'balancelabel',file))
                shutil.copy(os.path.join(path, 'images', file), os.path.join(path, 'balanceimage', file))
                count = count + 1
                print(count)

    # plt.plot(a)
    # plt.show()

def compare(path1,path2):
    dcm1 = pydicom.read_file(path1)
    img1 = dcm1.pixel_array

    dcm2 = pydicom.read_file(path2)
    img2 = dcm2.pixel_array

    img=np.abs(img1-img2)
    # print(np.sum(np.abs(img1-img2)))

    img[img < 1000] = 0
    img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
    img = img.astype(np.uint8)
    equ = cv.equalizeHist(img)
    cv.imwrite("unet.png", equ)



if __name__=="__main__":
    path1="D:\github\Data\SARI\Lung\M1\\bao_no"
    path2 = "D:\github\Data\SARI\Lung\M1\\bao_yes"
    # readFolder(path,"D:\\images\\images","D:\\images\\labels")

    imglist=os.listdir(path1)
    for i in range(171,len(imglist)):
        # dcmTopng(os.path.join(path,i),"unet.png")
        print(imglist[i])
        compare(os.path.join(path1,imglist[i]),os.path.join(path2,imglist[i]))
        break;

    # splitToImageLabel("D:\\images")