import cv2
import numpy as np
import math
import time
from src.CV.CVTopics import CVTopics
# TODO: update below once set up with new cam
distInch = (48/1133)*1.85  # inches per pixel conversion


class ArucoDetector:

    def __init__(self, observers, liveInference):
        # self.img_counter = 1
        self.observers = []
        for observer in observers:
            self.attachObserver(observer)
        # true means detecting with webcam, false is using stored images
        self.liveInference = liveInference

    def runModel(self):

        if self.liveInference:
            # replace the int with the camera index you want to use
            cap = cv2.VideoCapture(1)
            # wait for camera to connect before fetching frames
            time.sleep(1)
        # init pos value to avoid crashing if both tags not visible in first frame
        # the key is the aruco tag id and the three values are: x pos (pixels), y pos (pixels), and heading (degrees)
        # id 203 is the tag on the mqp robot and id 62 is on the opponent robot
        robotData = {203: [0, 0, 0], 23: [0, 0, 0]}

        while(1):
            if self.liveInference:
                _, image = cap.read()
            else:
                # replace path with the image you want to use
                # will crash without valid file
                image = cv2.imread('src/CV/tags/OnFiled.png')

            # choose aruco library to reference
            arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
            arucoParams = cv2.aruco.DetectorParameters_create()
            (origCorners, ids, rejected) = cv2.aruco.detectMarkers(
                image, arucoDict, parameters=arucoParams)

            # verify *at least* one ArUco marker was detected
            if len(origCorners) > 0:
                # flatten the ArUco IDs list
                ids = ids.flatten()

            # check if tags detected
            if ids is not None:
                # loop detected tags
                for (markerCorner, markerID) in zip(origCorners, ids):
                    # extract the tag corners (which are always returned in top-left, top-right, bottom-right, and bottom-left order)
                    corners = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners

                    # convert each of the (x, y) coordinate pairs to integers
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))

                    # draw the bounding box of the ArUCo detection
                    cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                    cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                    cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                    cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

                    # compute and draw the center (x, y) coordinates of the aruco tag
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                    heading = math.degrees(-1 * math.atan2(
                        topRight[1]-bottomRight[1], topRight[0] - bottomRight[0]))
                    robotData[markerID] = (cX, cY, heading)

                    # draw the aruco tag ID on the image
                    cv2.putText(image, str(markerID),
                                (topLeft[0], topLeft[1] -
                                 15), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 2)
                    #cv2.circle(image, (topLeft[0], topLeft[1]), radius = 5, color = (255,255,255), thickness = -1)

                # only update pos/heading when both detected
                    # otherwise target angles will be inaccurate
                if len(ids) == 2:
                    # update pos and heading
                    ourHeading = robotData[203][2]
                    ourPos = (robotData[203][0], robotData[203][1])
                    theirHeading = robotData[23][2]
                    theirPos = (robotData[23][0], robotData[23][1])
                    angleToTarget = math.degrees(-1 * math.atan2(
                        robotData[23][1] - robotData[203][1], robotData[23][0] - robotData[203][0]))
                    distToTarget = distInch * \
                        math.sqrt((robotData[203][1] - robotData[23][1]) **
                                  2 + (robotData[203][0] - robotData[23][0]) ** 2)

                    # print("targetHead: ", angleToTarget, "targetDist: ", distToTarget)

                    # send pos and heading
                    self.notifyObservers(CVTopics.HEADING, ourHeading)
                    self.notifyObservers(CVTopics.POSITION, ourPos)
                    self.notifyObservers(
                        CVTopics.OPPONENT_HEADING, theirHeading)
                    self.notifyObservers(CVTopics.OPPONENT_POSITION, theirPos)
                    self.notifyObservers(
                        CVTopics.TARGET_HEADING, angleToTarget)
                    self.notifyObservers(
                        CVTopics.TARGET_DISTANCE, distToTarget)

                    # save annotated image to be pulled by gui
                    cv2.imwrite("output.jpg", image)

        # cv2.destroyAllWindows()

    def notifyObservers(self, topic, value):
        for observer in self.observers:
            observer.notify(topic, value)

    def attachObserver(self, observer):
        self.observers.append(observer)
