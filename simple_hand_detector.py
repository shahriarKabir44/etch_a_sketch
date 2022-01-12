import cv2
import mediapipe as mp
import time
import random
from hand_detection_module import HandDetector

DRAW_MODE = 0
ERASER_MODE = 1
DO_NOTHING_MODE = 2


def canTakePoint(point1, point2, minimumDistance):
    x1, y1 = point1
    x2, y2 = point2
    return (x1-x2)**2 + (y1-y2)**2 >= minimumDistance**2


def drawLineSegments(points: list[list[int]], imageObject):
    for n in range(1, len(points)):
        x1, y1 = points[n]
        x2, y2 = points[n-1]
        cv2.line(imageObject, (x1, y1), (x2, y2), (0, 0, 254), 15)


def drawCurveSegments(line_segments, imageObject):
    # print('len', *(line_segments), sep=' ')
    for curveSegment in line_segments:
        drawLineSegments(curveSegment, imageObject)


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
    line_segments = [[]]
    points = line_segments[0]

    lastInserted = None
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
                            lastInserted = leftIndex
                            line_segments[-1].append(lastInserted)
                        elif canTakePoint(lastInserted, leftIndex, 15):
                            lastInserted = leftIndex
                            # print('inserted', random.randint(1, 10))
                            line_segments[-1].append(lastInserted)
                        previousMode = DRAW_MODE

                    elif drawType == DO_NOTHING_MODE:
                        if previousMode != DO_NOTHING_MODE:
                            lastInserted = None
                            line_segments.append([])
                        previousMode = DO_NOTHING_MODE
                    else:

                        for segment in range(len(line_segments)):
                            validPlaces = []
                            for n in range(len(line_segments[segment])):
                                if canTakePoint(leftIndex, line_segments[segment][n], 25):
                                    validPlaces.append(
                                        line_segments[segment][n])
                            line_segments[segment] = validPlaces
                        lastInserted = None
                        if previousMode != ERASER_MODE:
                            line_segments.append([])
                        previousMode = ERASER_MODE
        drawCurveSegments(line_segments, img)
        # print(points)
        # cv2.putText(img, text="abcd", org=(10, 70), color=(255, 0, 255),
        #             fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=3)
        cv2.imshow("image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
