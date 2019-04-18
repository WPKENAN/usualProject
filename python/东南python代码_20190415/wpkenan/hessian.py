import cv2
import cv2 as cv

imagename="C:\\Users\\admin\Desktop\\2.png"
image = cv2.imread(imagename, 0)
blood = cv2.normalize(image.astype('double'), None, 0.0, 1.0, cv2.NORM_MINMAX)  # Convert to normalized floating point
# 用normalize函数导致图像中的像素为浮点型，导致后面用HoughLinesP函数时出错？
outIm = FrangiFilter2D(blood)
edges = outIm * (10000)
# edges=outIm*(10000).astype(np.int8)  # 这样也不行

cv2.imshow('Frangi Filter Result', edges)

minLineLength = 200
maxLineGap = 50
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, minLineLength, maxLineGap)