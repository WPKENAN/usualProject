import cv2 as cv
import cv2
import numpy as np
import os


def calcAndDrawHist(image, color):
    hist = cv2.calcHist([image], [0], None, [256], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    histImg = np.zeros([256, 256, 3], np.uint8)
    hpt = int(0.9 * 256);

    for h in range(256):
        intensity = int(hist[h] * hpt / maxVal)
        cv2.line(histImg, (h, 256), (h, 256 - intensity), color)

    return histImg;


if __name__ == '__main__':
    img = cv2.imread(".\\data\\144.jpg")
    img=cv2.resize(img,(600, 600), interpolation=cv.INTER_CUBIC)
    img=img[200:400,200:400,:]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # print(hsv)

    s=90;
    v=90;
    color=['red','green','blue','yellow']
    rgby=[]
    for c in range(4):
        if c==0:
            # 红色
            lower_bule = np.array([140, s, v])
            upper_blue = np.array([255, 255, 255])
            # 根据阀值构建掩模
            mask = cv2.inRange(hsv, lower_bule, upper_blue)
            lower_bule = np.array([0, s, v])
            upper_blue = np.array([10, 255, 255])
            # 根据阀值构建掩模
            mask = cv2.inRange(hsv, lower_bule, upper_blue)+mask
        elif c==1:
            # 绿色
            lower_bule = np.array([30, s, v])
            upper_blue = np.array([90, 255, 255])
            # 根据阀值构建掩模
            mask = cv2.inRange(hsv, lower_bule, upper_blue)
        elif c==2:
            # 蓝色
            lower_bule = np.array([110, s, v])
            upper_blue = np.array([135, 255, 255])
            # 根据阀值构建掩模
            mask = cv2.inRange(hsv, lower_bule, upper_blue)
        elif c==3:
            #黄
            lower_bule = np.array([0, 0, 200])
            upper_blue = np.array([256, 30, 255])
            # 根据阀值构建掩模
            mask = cv2.inRange(hsv, lower_bule, upper_blue)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv.erode(np.copy(mask), kernel);
        # 对原图和淹模进行位运算
        res = cv2.bitwise_and(img, img, mask=mask)
        # print(sum(sum(sum(res.astype('int')))))
        rgby.append([sum(sum(sum(res.astype('int')))),c])
        cv2.imshow('frame', img)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        cv2.waitKey(1000)

    rgby.sort(reverse=-1)
    print(rgby)
    if rgby[0][1]<3:
        if rgby[0][0]<25000:
            print("没有开灯")
        else:
            print("color is : {}".format(color[rgby[0][1]]))
    else:
        if rgby[0][0]<30000:
            print("没有开灯")
        elif rgby[1][0]>25000:
            print("color is : {}".format(color[rgby[1][1]]))
        else:
            print("yellow")
        # pass


