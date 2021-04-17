import cv2
import time
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
time.sleep(1)
while(1):
    _, image = cap.read()
    cv2.imshow("window", image)
    time.sleep(.2)
    cv2.waitKey(0)