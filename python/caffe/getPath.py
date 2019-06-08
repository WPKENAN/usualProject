# coding:utf-8

import cv2
import os


def IsSubString(SubStrList, Str):  # 判断SubStrList的元素
    flag = True  # 是否在Str内
    for substr in SubStrList:
        if not (substr in Str):
            flag = False

    return flag


def GetFileList(FindPath, FlagStr=[]):  # 搜索目录下的子文件路径
    FileList = []
    FileNames = os.listdir(FindPath)
    if len(FileNames) > 0:
        for fn in FileNames:
            if len(FlagStr) > 0:
                if IsSubString(FlagStr, fn):  # 不明白这里判断是为了啥
                    fullfilename = os.path.join(FindPath, fn)
                    FileList.append(fullfilename)
            else:
                fullfilename = os.path.join(FindPath, fn)
                FileList.append(fullfilename)

    if len(FileList) > 0:
        FileList.sort()

    return FileList


train_txt = open('train.txt', 'w')  # 制作标签数据
classList = ['0', '1', '2', '3', '4']
for idx in range(len(classList)):
    imgfile = GetFileList('train/' + classList[idx])  # 将数据集放在与.py文件相同目录下
    for img in imgfile:
        srcImg = cv2.imread(img);
        resizedImg = cv2.resize(srcImg, (28, 28))
        cv2.imwrite(img, resizedImg)
        strTemp = img + ' ' + classList[idx] + '\n'  # 用空格代替转义字符 \t
        train_txt.writelines(strTemp)
train_txt.close()

test_txt = open('val.txt', 'w')  # 制作标签数据
for idx in range(len(classList)):
    imgfile = GetFileList('val/' + classList[idx])
    for img in imgfile:
        srcImg = cv2.imread(img);
        resizedImg = cv2.resize(srcImg, (28, 28))
        cv2.imwrite(img, resizedImg)
        strTemp = img + ' ' + classList[idx] + '\n'  # 用空格代替转义字符 \t
        test_txt.writelines(strTemp)
test_txt.close()

print("成功生成文件列表")
