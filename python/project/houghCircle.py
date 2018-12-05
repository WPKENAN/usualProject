import cv2
image=cv2.imread("C:/Users\Anzhi\Desktop\github\Data\hough1.png",0)
# cv2.imshow("main",image)
# cv2.waitKey(0)

temp,image=cv2.threshold(image,thresh=150,maxval=255,type=cv2.THRESH_BINARY);
image=cv2.Canny(image,150,255);
# cv2.imshow('Circle', image)
# cv2.waitKey(0)
# exit(0)
circles=cv2.HoughCircles(image, method=cv2.HOUGH_GRADIENT, dp=10,minDist=1,minRadius=0,maxRadius=40)

print(len(circles[0]))
print(circles[0])
for c in circles:
   for x,y,r in c:
      cv2.circle(image, (x,y), r, (255, 255, 255), 2)
      cv2.imshow('Circle', image)
      cv2.waitKey(3000)

cv2.waitKey(0)
cv2.destroyAllWindows()