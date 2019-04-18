import cv2 as cv
import numpy as np
import os


def myFindContours(imgOriginal,binary):
    img=imgOriginal.copy()
    image,cnts, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    tmp = imgOriginal.copy()
    for cnt in cnts:
        x_max=max(cnt[:,0,0]);
        x_min=min(cnt[:,0,0]);
        y_max=max(cnt[:,0,1]);
        y_min=min(cnt[:,0,1]);

        cv.rectangle(tmp, (max(0, x_min - 10), max(0, y_min - 10)),(min(img.shape[0], x_max + 10), min(img.shape[1], y_max + 10)), (0, 0, 255), 1)
        # cv.rectangle(img,,(0,0,255),1)
        cv.imwrite("9_all_cnts.jpg", tmp)

    for cnt in cnts:
        if len(cnt)<=100 and len(cnt)>=0:

            x_max=max(cnt[:,0,0]);
            x_min=min(cnt[:,0,0]);
            y_max=max(cnt[:,0,1]);
            y_min=min(cnt[:,0,1]);
            if (x_max - x_min)*(y_max-y_min)>3200:
                continue
            print((x_max - x_min)*(y_max-y_min))

            cv.rectangle(img, (max(0, x_min - 10), max(0, y_min - 10)),(min(img.shape[0], x_max + 10), min(img.shape[1], y_max + 10)), (0, 0, 255), 1)
            # cv.rectangle(img,,(0,0,255),1)
        cv.imwrite("10_result.jpg", img)
        cv.imshow("img", np.hstack((imgOriginal, img)))
    # waitKey(0)

def mySobel(imgOriginal):
    img=cv.cvtColor(imgOriginal, cv.COLOR_BGR2GRAY);
    # cv.imwrite("COLOR_BGR2GRAY.jpg", img)
    x=cv.Sobel(img,cv.CV_16S,1,0);
    y=cv.Sobel(img,cv.CV_16S,0,1);
    absX = cv.convertScaleAbs(x)
    cv.imwrite("3_sobel(x).jpg", absX)
    absY = cv.convertScaleAbs(y)
    cv.imwrite("4_sobel(y).jpg", absY)
    dst = cv.addWeighted(absX, 1, absY, 1, 0)
    cv.imwrite("5_sobel(x)+sobel(y).jpg", dst)


    ret, binary = cv.threshold(dst, 47, 255, cv.THRESH_BINARY)

    cv.imwrite("6_binary.jpg", binary)

    kernel = np.ones((2, 2), np.uint8)
    binary = cv.erode(np.copy(binary), kernel);
    cv.imwrite("7_erode2x2.jpg", binary)
    cv.imshow("binary1", binary)

    kernel = np.ones((50, 50), np.uint8)
    binary = cv.dilate(np.copy(binary), kernel);
    cv.imwrite("8_dilate50x50.jpg", binary)

    cv.imshow("binary", binary)
    myFindContours(np.copy(imgOriginal),np.copy(binary))

    dist = cv.distanceTransform(binary, cv.DIST_L2, 5)
    xy = np.hstack((absX, absY,binary))
    dist=dist.astype(np.uint8)
    max_=np.max(dist)
    print(np.max(dist))
    for i in range(len(dist)):
        for j in range(len(dist[0])):
            dist[i][j]=int(dist[i][j]/max_*255)
    result = np.hstack((img, dist))
    # print(img.dtype.type)
    # print(dist.dtype.type)
    # imshow("xysobel", xy)
    # imshow("img_dist",result)
    # plt.imshow(dist, cmap='gray')
    # plt.show()
    cv.waitKey(0)
    cv.destroyAllWindows()

def main():
    print("hello")
    folder="D:\github\Data\Paint\keli\\";
    for filename in os.listdir(folder):
        print(filename)
        if filename.split('.')[1].lower() in ['jpg','png','bmp']:
            filename = folder+"\\"+filename
            # filename = 'D:\github\Data\Paint\keli\\test.png'
            img = cv.imread(filename);
            # img=cvtColor(img,COLOR_BGR2GRAY)
            img = cv.resize(img, (600, 600), interpolation=cv.INTER_CUBIC);
            cv.imwrite("1_600x600.jpg", img)
            # imshow("img", img)
            # waitKey(0)
            # 均值滤波
            img1 = cv.blur(img, (5, 7))
            # 中值滤波
            img2 = cv.medianBlur(img, 3)
            # 高斯滤波
            img3 = cv.GaussianBlur(img, (7, 7,), 0)
            # 拉普拉斯
            img4 = img - np.uint8(np.absolute(cv.Laplacian(img, cv.CV_16S, ksize=1)));
            # mySobel(img)
            cv.imwrite("2_blur5x7.jpg",img1)
            mySobel(img1)

if __name__=="__main__":
    print("hello")
    main()