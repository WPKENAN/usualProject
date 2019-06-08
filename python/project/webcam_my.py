import cv2
import numpy
import matplotlib.pyplot as plot
cap = cv2.VideoCapture(0)
i=0
while(1):
    i+=1
    print(i)
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
