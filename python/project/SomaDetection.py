import cv2
image=cv2.imread("C:/Users\Anzhi\Desktop\github\Data\hough1.png",0)
# print(image.shape)
h,w=image.shape;
meanGlobal=image.mean()
stdGlobal=image.std()
meanStdEvery=[];
stepWidth=25;

for centerX in range(0,h,stepWidth):
    for centerY in range(0,w,stepWidth):
        startX=int(max((centerX-stepWidth/2),0))
        startY=int(max((centerY-stepWidth/2),0));
        endX=int(min((centerX+stepWidth/2+1),h))
        endY=int(min((centerY+stepWidth/2+1),w))
        # if len(image[startX:endX, startY:endY])==0:
        #     print(image[startX:endX, startY:endY])
        #     print([[startX, endX], [startY, endY]])

        meanStdEvery.append([centerX,centerY,image[startX:endX,startY:endY].mean(),image[startX:endX,startY:endY].std()])
        # cv2.circle(image,(i,j),25,(255,255,255),1)

print([h,w])
print(meanGlobal)
print(meanStdEvery)

meanStdEvery.sort(key=lambda x:x[-2],reverse=True)
print(meanStdEvery);

meanStdEvery.sort(key=lambda x:x[-1])
for gray in meanStdEvery:
    if gray[2]>meanGlobal*4:
        print(gray)
        cv2.circle(image,(gray[0],gray[1]),stepWidth,(255,255,255),1)
        break;

# print(meanGlobal)
cv2.imshow("main",image)
cv2.waitKey(0)
cv2.destroyAllWindows()