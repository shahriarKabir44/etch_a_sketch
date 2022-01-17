import cv2
import mediapipe as mp
import time
import random
from hand_detection_module import HandDetector
from utility_classes import Point, LinkedList

DRAW_MODE = 0
ERASER_MODE = 1
DO_NOTHING_MODE = 2


def canTakePoint(point1, point2, minimumDistance):
    x1, y1 = point1
    x2, y2 = point2
    return (x1-x2)**2 + (y1-y2)**2 >= minimumDistance**2


def getCursorMode(thumbLocation, indexFingerLocation, threshold=15):
    x1, y1 = thumbLocation
    x2, y2 = indexFingerLocation
    if not canTakePoint(thumbLocation, indexFingerLocation, threshold):
        return ERASER_MODE
    if y1 < y2:
        return DO_NOTHING_MODE
    if y2 < y1:
        return DRAW_MODE


def main():
    cap = cv2.VideoCapture(0)
    handDetector = HandDetector()
    line_segments = LinkedList(Point(0, 0))
    lastInserted = line_segments.head
    lastInserted.isWithinSegment = False
    previousMode = None
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        #img = cv2.resize(img, (800, 800))
        handDetector.findHands(img, 1 == 1)
        leftIndex = handDetector.findLandmarkPosition(
            img, shouldHighlight=True, landmarkNumber=8)

        rightThumbPosition = None
        rightIndexPosition = None
        if handDetector.multi_hand_landmarks and len(handDetector.multi_hand_landmarks) >= 2:
            rightThumbPosition = handDetector.findLandmarkPosition(
                img, handNumber=1, landmarkNumber=4, shouldHighlight=True, color=(0, 102, 255))

            rightIndexPosition = handDetector.findLandmarkPosition(
                img, handNumber=1, landmarkNumber=8, shouldHighlight=True, color=(51, 204, 51))

        if leftIndex:
            if rightThumbPosition:
                if rightIndexPosition:
                    drawType = getCursorMode(
                        rightThumbPosition, rightIndexPosition, threshold=20)
                    # print(drawType)
                    if drawType == DRAW_MODE:
                        if lastInserted == None:
                            # print('inserted1', random.randint(1, 10))
                            lastInserted = Point(leftIndex[0], leftIndex[1])
                            line_segments .append(lastInserted)
                        elif canTakePoint([lastInserted.x, lastInserted.y], leftIndex, 15) and lastInserted.isWithinSegment:
                            lastInserted = Point(leftIndex[0], leftIndex[1])
                            # print('inserted', random.randint(1, 10))
                            line_segments .append(lastInserted)
                        elif lastInserted.isWithinSegment == False:
                            lastInserted = Point(leftIndex[0], leftIndex[1])
                            # print('inserted', random.randint(1, 10))
                            line_segments .append(lastInserted)
                        previousMode = DRAW_MODE

                    elif drawType == DO_NOTHING_MODE:
                        if previousMode != DO_NOTHING_MODE:
                            lastInserted.isWithinSegment = False
                        previousMode = DO_NOTHING_MODE
                    else:

                        line_segments.findAndRemove(leftIndex)
                        lastInserted.isWithinSegment = False
                        previousMode = ERASER_MODE

        line_segments.draw(img)
        # print(points)
        # cv2.putText(img, text="abcd", org=(10, 70), color=(255, 0, 255),
        #             fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=3)
        cv2.imshow("image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
