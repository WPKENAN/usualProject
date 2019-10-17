import cv2 as cv
import numpy as np


if __name__=="__main__":
    img=cv.imread("3.bmp")
    print(img.shape)
    width=512;
    height=516
    interval_w=26;
    interval_h=0;

    # l=99
    # c=79
    # cv.imshow("main {},{}".format(c,l),img[c:c+height,l:l+width,:])

    # c=c+height+interval_h
    # l=l+width+interval_w
    # cv.imshow("main {},{}".format(c,l), img[c:c+height, l:l+width, :])
    #
    # l=l+width+interval_w
    # cv.imshow("main{}".format(l), img[:, l:l + width, :])

    startl=99
    startc=79
    for j in range(4):
        for i in range(3):
            l=startl+i*(width+interval_w)
            c=startc+j*(height+interval_h)
            # cv.imshow("main {},{}".format(c, l), img[c:c + height, l:l + width, :])
            # cv.waitKey(0)

            # img[c:c + height, l:l + width, :]
            cv.imwrite("{}.jpg".format(j*3+i),img[c:c + height, l:l + width, :])


    img=np.zeros((516,512,3))
    for i in range(1,11):
        print(i)
        b = cv.imread("{}.jpg".format(i-1),0)
        g = cv.imread("{}.jpg".format(i),0)
        r = cv.imread("{}.jpg".format(i+1),0)
        print(b.shape)



        img[:b.shape[0],:b.shape[1],0] = b;
        img[:g.shape[0], :g.shape[1], 1] = g;
        img[:r.shape[0], :r.shape[1], 2] = r;
        cv.imwrite("{}_{}_{}.png".format(i-1,i,i+1),img)





