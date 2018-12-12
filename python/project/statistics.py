import numpy as np
import matplotlib.pyplot as plt
import cv2

filePath="D:\\github\\Data\\gray.txt";
file=open(filePath);
content=file.readlines();

for i in range(len(content)):
    content[i]=(content[i].strip('\n'));

content=np.array(content,dtype="uint8")
ret,th=cv2.threshold(content,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU);
print(ret)
gray=[0]*256
for i in content:
    gray[i]=gray[i]+1;


print(gray.index(max(gray)))
print(max(gray))

plt.figure();
plt.scatter(range(256),gray);
plt.show()