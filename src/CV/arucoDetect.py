import cv2
import numpy as np
import math
from src.CV.CVTopics import CVTopics
distInch = 48/1133 # inches per pixel conversion

class ArucoDetector:

    def __init__(self, observers):
        # self.img_counter = 1
        self.observers = []
        for observer in observers:
            self.attachObserver(observer)

    def runModel(self):

        # uncomment below for live detection
        #cap = cv2.VideoCapture(0)
        idStore = {}
        while(1):


            # top line is for webcam bottom is for static image
            #_, frame = cap.read()
            image = cv2.imread('src/CV/tags/OnFiled.png')

            arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
            arucoParams = cv2.aruco.DetectorParameters_create()
            (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

            # verify *at least* one ArUco marker was detected
            if len(corners) > 0:
                # flatten the ArUco IDs list
                ids = ids.flatten()
                # loop over the detected ArUCo corners
            for (markerCorner, markerID) in zip(corners, ids):
                # extract the marker corners (which are always returned in
                # top-left, top-right, bottom-right, and bottom-left order)
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                # draw the bounding box of the ArUCo detection
                cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
                # compute and draw the center (x, y)-coordinates of the ArUco
                # marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                heading = math.degrees(-1 * math.atan2(topRight[1]-bottomRight[1], topRight[0]- bottomRight[0]))
                idStore[markerID] = (cX, cY, heading)
                # draw the ArUco marker ID on the image
                cv2.putText(image, str(markerID),
                    (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
                cv2.circle(image, (topLeft[0], topLeft[1]), radius = 5, color = (255,255,255), thickness = -1)
                # print("[INFO] ArUco marker ID: {}".format(markerID), "pos: (", cX, ",", cY, "), heading: ", heading)
                # show the output image

            ourHeading = idStore[203][2]
            ourPos = (idStore[203][0], idStore[203][1])
            theirHeading = idStore[62][2]
            theirPos = (idStore[62][0], idStore[62][1])
            angleToTarget = math.degrees(-1 * math.atan2(idStore[62][1] - idStore[203][1], idStore[62][0] - idStore[203][0]))
            distToTarget = distInch * math.sqrt((idStore[203][1] - idStore[62][1]) ** 2 +  (idStore[203][0] - idStore[62][0]) ** 2)
            # print("targetHead: ", angleToTarget, "targetDist: ", distToTarget)

            self.notifyObservers(CVTopics.HEADING, ourHeading)
            self.notifyObservers(CVTopics.POSITION, ourPos)
            self.notifyObservers(CVTopics.OPPONENT_HEADING, theirHeading)
            self.notifyObservers(CVTopics.OPPONENT_POSITION, theirPos)
            self.notifyObservers(CVTopics.TARGET_HEADING, angleToTarget)
            self.notifyObservers(CVTopics.TARGET_DISTANCE, distToTarget)

        #     cv2.imshow('image', image)
        #     cv2.imwrite("output.jpg", image)
        #     cv2.waitKey(10)

        # cv2.destroyAllWindows()

    def notifyObservers(self, topic, value):
        for observer in self.observers:
            observer.notify(topic, value)


    def attachObserver(self, observer):
        self.observers.append(observer)