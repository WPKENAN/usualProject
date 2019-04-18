import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import

def Least_squares(x,y):
    x_ = x.mean()
    y_ = y.mean()
    m = np.zeros(1)
    n = np.zeros(1)
    k = np.zeros(1)
    p = np.zeros(1)
    for i in np.arange(50):
        k = (x[i]-x_)* (y[i]-y_)
        m += k
        p = np.square( x[i]-x_ )
        n = n + p
    a = m/n
    b = y_ - a* x_
    print(a, b)
    y1 = a * x + b
    return a,b
    # plt.figure(figsize=(10, 5), facecolor='w')
    # plt.plot(x, y, 'ro', lw=2, markersize=6)
    # plt.plot(x, y1, 'r-', lw=2, markersize=6)
    # plt.grid(b=True, ls=':')
    # plt.xlabel(u'X', fontsize=16)
    # plt.ylabel(u'Y', fontsize=16)
    # plt.show()

def sobel(imgOriginal,p=0.5):
    img = cv.cvtColor(imgOriginal, cv.COLOR_BGR2GRAY);
    x = cv.Sobel(img, cv.CV_16S, 1, 0);
    y = cv.Sobel(img, cv.CV_16S, 0, 1);
    absX = cv.convertScaleAbs(x)
    absY = cv.convertScaleAbs(y)
    dst = cv.addWeighted(absX, p, absY, 1-p, 0)
    ret, binary = cv.threshold(dst, 26, 255, cv.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    binary = cv.erode(np.copy(binary), kernel);

    cv.imshow('dts',binary);
    cv.waitKey(0);
    cv.destroyAllWindows();
    return binary

def preDealImg():
    path="C:\\Users\Anzhi\Desktop\\1.png";
    img=cv.imread(path);
    # img = cv.cvtColor(img, cv.COLOR_BGR2GRAY);
    return img;
def main():
    img=preDealImg();
    dstX=sobel(img,10000);
    dstY=sobel(img,-10000)

    image, cnts, hierarchy = cv.findContours(dstX, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE);
    linex=[];
    for cnt in cnts:
        if len(cnt)>=100:
            linex.append(np.zeros((cnt.shape[0],cnt.shape[2])));
            for i in range(len(cnt)):
                linex[-1][i,0]=cnt[i,0,0];
                linex[-1][i,1]=cnt[i,0,1];
    print(linex)

    liney=[];
    image, cnts, hierarchy = cv.findContours(dstY, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE);
    count = 0;
    for cnt in cnts:
        if len(cnt)>=100:
            liney.append(np.zeros((cnt.shape[0],cnt.shape[2])));
            for i in range(len(cnt)):
                liney[-1][i,0]=cnt[i,0,0];
                liney[-1][i,1]=cnt[i,0,1];


    ab=[]
    ab.append(Least_squares(linex[0][:,0],linex[0][:,1]))
    ab.append(Least_squares(linex[1][:,0],linex[1][:,1]))

    ab.append(Least_squares(liney[0][:, 0], liney[0][:, 1]))
    ab.append(Least_squares(liney[1][:, 0], liney[1][:, 1]))

    theat1=





    print()





    # x = np.linspace(0, 30, num=50)
    # y = 0.2 * x + [np.random.random() for _ in range(50)]
    # Least_squares(x,y)

if __name__ == '__main__':
    main()
