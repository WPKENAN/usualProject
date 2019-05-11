import cv2 as cv
from PIL import Image
import os



for i in range(50):
    downSample = 256
    folder="D:\github\Data\GlandCeildata\\train_simple\Image"
    img=cv.imread(folder+"\\{}.bmp".format(i))
    img = cv.resize(img,(downSample, downSample),interpolation=cv.INTER_CUBIC)
    outfolder="D:\github\Data\GlandCeildata\\train_128\Image"
    cv.imwrite(outfolder+"\\{}.bmp".format(i),img)

    folder = "D:\github\Data\GlandCeildata\\train_simple\Mask"
    img = cv.imread(folder + "\\{}.bmp".format(i))
    img = cv.resize(img, (downSample, downSample), interpolation=cv.INTER_CUBIC)
    outfolder = "D:\github\Data\GlandCeildata\\train_128\Mask"
    cv.imwrite(outfolder + "\\{}.bmp".format(i), img)

for i in range(5):
    downSample = 256
    folder="D:\github\Data\GlandCeildata\\test_simple\Image"
    img=cv.imread(folder+"\\{}.bmp".format(i))
    img = cv.resize(img,(downSample, downSample),interpolation=cv.INTER_CUBIC)
    outfolder="D:\github\Data\GlandCeildata\\test_128\Image"
    cv.imwrite(outfolder+"\\{}.bmp".format(i),img)

    folder = "D:\github\Data\GlandCeildata\\test_simple\Mask"
    img = cv.imread(folder + "\\{}.bmp".format(i))
    img = cv.resize(img, (downSample, downSample), interpolation=cv.INTER_CUBIC)
    outfolder = "D:\github\Data\GlandCeildata\\test_128\Mask"
    cv.imwrite(outfolder + "\\{}.bmp".format(i), img)