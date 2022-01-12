import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, static_image_mode=False, max_num_hands=2, model_complexity=1, min_detection_confidence=.5, min_tracking_confidence=.5) -> None:
        self.static_image_mode = static_image_mode,
        self.max_num_hands = max_num_hands,
        self.model_complexity = model_complexity,
        self.min_detection_confidence = min_detection_confidence,
        self.min_tracking_confidence = min_tracking_confidence

        self.multi_hand_landmarks = []
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(
            static_image_mode, max_num_hands, model_complexity, min_detection_confidence, min_tracking_confidence)

    def findHands(self, img, shouldDraw=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self. hands.process(imgRGB)

        # print(result.multi_hand_landmarks)

        self.multi_hand_landmarks = result.multi_hand_landmarks
        if self.multi_hand_landmarks:
            for hand in self.multi_hand_landmarks:

                if shouldDraw:
                    self.mpDraw.draw_landmarks(
                        img, hand, self.mpHands.HAND_CONNECTIONS)

    def findhandPosition(self, img, landMarkNumber=0, handNumber=0, shouldDraw=False):
        landmarkList = []
        hgt, wdt, c = img.shape
        if self.multi_hand_landmarks:
            # print(self.multi_hand_landmarks)
            if len(self.multi_hand_landmarks) >= handNumber:
                for id, lm in enumerate(self.multi_hand_landmarks[handNumber].landmark):
                    cx, cy = int(lm.x*wdt), int(lm.y*hgt)
                    landmarkList.append([id, cx, cy])
                if shouldDraw:
                    cv2.circle(img, (int(self.multi_hand_landmarks[handNumber].landmark[landMarkNumber].x*wdt), int(self.multi_hand_landmarks[handNumber].landmark[landMarkNumber].y*hgt)), 15,
                               (255, 0, 255), cv2.FILLED)
        return landmarkList

    def findLandmarkPosition(self, imageObject, landmarkNumber=0, handNumber=0, shouldHighlight=False, color=(255, 0, 255)):
        landmarkLocation = None
        hgt, wdt, c = imageObject.shape
        if self.multi_hand_landmarks:
            # print(self.multi_hand_landmarks)
            if len(self.multi_hand_landmarks) >= handNumber:
                if len(self.multi_hand_landmarks[handNumber].landmark) >= landmarkNumber:
                    lm = self.multi_hand_landmarks[handNumber].landmark[landmarkNumber]
                    cx, cy = int(lm.x*wdt), int(lm.y*hgt)

                    landmarkLocation = [cx, cy]

                if shouldHighlight:
                    cv2.circle(imageObject, (int(self.multi_hand_landmarks[handNumber].landmark[landmarkNumber].x*wdt), int(self.multi_hand_landmarks[handNumber].landmark[landmarkNumber].y*hgt)), 15,
                               color, cv2.FILLED)
        return landmarkLocation
