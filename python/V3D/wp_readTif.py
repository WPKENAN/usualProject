import cv2 as cv
from libtiff import TIFF
import numpy as np

tif = TIFF.open('D:\\github\Data\\23.tif', mode='r')
# img = tif.read_image()  # 此时img为一个numpy.array
# print(img.shape)
count=0;
imageAll=np.array([0])
for image in tif.iter_images():
    if count==0:
        imageAll=image;
    else:
        imageAll=np.dstack((imageAll,image))
        # print(image.shape)
    count=count+1
    cv.imshow("main",image)
    cv.waitKey(0)
    cv.destroyAllWindows()

print("z={}".format(count))
print(imageAll.shape)