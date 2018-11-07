import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# path="C:/Users/Anzhi/Desktop/场.png"
path="D:\wp\微信文件夹\WeChat Files\WPKENAN\Files\计算性导论\题目\\16_1.jpg"
print(path)
image = cv.imdecode(np.fromfile(path,dtype=np.uint8),-1)
# write
# cv.imencode('.jpg',img)[1].tofile(path)
print(image.shape)
# print(image)

r,g,b=cv.split(image)
res=cv.resize(g,(1800,900),interpolation=cv.INTER_CUBIC)

plt.hist(res.ravel(),256)
plt.show()
thresh,res=cv.threshold(res,thresh=150,maxval=255,type=cv.THRESH_BINARY);
print(res)

cv.imshow("main",res)
cv.waitKey(0)