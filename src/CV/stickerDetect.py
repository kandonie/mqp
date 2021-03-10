import cv2
import numpy as np
import math
from src.CV.CVTopics import CVTopics

class CV:
    """
    the computer representation of the drive
    """

    def __init__(self, observers):
        self.observers = []
        for observer in observers:
            self.attachObserver(observer)


    def runModel(self):
        # uncomment below for live detection
        #cap = cv2.VideoCapture(0)

        while(1):

            # top line is for webcam bottom is for static image
            #_, frame = cap.read()
            frame = cv2.imread('src/CV/stickers/image-036.jpeg')
            # print(np.shape(frame))
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            ## find green centroid

            # define range of green color in HSV
            lower_g = np.array([30,52,72])
            upper_g = np.array([102,255,255])

            # Threshold the HSV image to get only green colors
            mask_g = cv2.inRange(hsv, lower_g, upper_g)

            # Bitwise-AND mask and original image
            res_g = cv2.bitwise_and(frame,frame, mask= mask_g)
            # cv2.imshow('green', res_g)

            # calculate moments of binary image
            M = cv2.moments(mask_g)

            # calculate x,y coordinate of center
            cXg = int(M["m10"] / M["m00"])
            cYg = int(M["m01"] / M["m00"])

            # put text and highlight the center
            cv2.circle(frame, (cXg, cYg), 5, (255, 255, 255), -1)
            cv2.putText(frame, "green", (cXg - 25, cYg - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            ## find purple centroid

            # define range of purple color in HSV
            lower_p = np.array([120, 90, 90])
            upper_p = np.array([150,255,255])

            # Threshold the HSV image to get only purple colors
            mask_p = cv2.inRange(hsv, lower_p, upper_p)

            # Bitwise-AND mask and original image
            res_p = cv2.bitwise_and(frame,frame, mask= mask_p)
            # cv2.imshow('purp', res_p)

            # calculate moments of binary image
            M = cv2.moments(mask_p)

            # calculate x,y coordinate of center
            cXp = int(M["m10"] / M["m00"])
            cYp = int(M["m01"] / M["m00"])

            # put text and highlight the center
            cv2.circle(frame, (cXp, cYp), 5, (255, 255, 255), -1)
            cv2.putText(frame, "purp", (cXp - 25, cYp - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            ## heading and pos

            print("position", cXp, cYp)

            heading = -1 * math.atan2(cYp-cYg, cXp - cXg)
            print("heading", heading)
            cv2.putText(frame, str(heading), (cXp - 100, cYp - 100),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # notify observers of current heading and position
            self.notifyObservers(CVTopics.HEADING, heading)
            self.notifyObservers(CVTopics.X_POSITION, cXp)
            self.notifyObservers(CVTopics.Y_POSITION, cYp)

        #     cv2.imshow('frame', frame)
            cv2.imwrite("output.jpg", frame)
        #     k = cv2.waitKey(5) & 0xFF
        #     if k == 27:
        #         break

        # cv2.destroyAllWindows()


    def notifyObservers(self, topic, value):
        for observer in self.observers:
            observer.notify(topic, value)


    def attachObserver(self, observer):
        self.observers.append(observer)