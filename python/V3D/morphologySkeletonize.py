from skimage import morphology,draw
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# #创建一个二值图像用于测试
# image = np.zeros((400, 400))
#
# #生成目标对象1(白色U型)
# image[10:-10, 10:100] = 1
# image[-100:-10, 10:-10] = 1
# image[10:-10, -100:-10] = 1
#
# #生成目标对象2（X型）
# rs, cs = draw.line(250, 150, 10, 280)
# for i in range(10):
#     image[rs + i, cs] = 1
# rs, cs = draw.line(10, 150, 250, 280)
# for i in range(20):
#     image[rs + i, cs] = 1
#
# #生成目标对象3（O型）
# ir, ic = np.indices(image.shape)
# circle1 = (ic - 135)**2 + (ir - 150)**2 < 30**2
# circle2 = (ic - 135)**2 + (ir - 150)**2 < 20**2
# image[circle1] = 1
# image[circle2] = 0

image=cv.imread("C:\\Users\\Anzhi\\Desktop\\2.png");
b,g,r=cv.split(image)
print(np.shape(image))
_,bBinary=cv.threshold(b,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
cv.imshow("b",bBinary);
cv.waitKey(1000)
_,b=cv.threshold(bBinary,0,1,cv.THRESH_BINARY)
# for i in range(len(b)):
#     for j in range(len(b[0])):
#         if b[i,j]!=0:
#             # print(b[i,j])

# print(b)
#实施骨架算法
skeleton =morphology.skeletonize(b)

#显示结果
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))

ax1.imshow(image, cmap=plt.cm.gray)
ax1.axis('off')
ax1.set_title('original', fontsize=20)

ax2.imshow(skeleton, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('skeleton', fontsize=20)

fig.tight_layout()
plt.show()

