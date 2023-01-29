import cv2
import mediapipe as mp
import time
import math
import numpy as np


class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):


        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose

        self.pose = self.mpPose.Pose(self.mode
                                     , min_detection_confidence=0.5
                                     , min_tracking_confidence=0.5
                                     )

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):

        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # print(angle)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle


def main():
    cap = cv2.VideoCapture("KneeBendVideo.mp4")
    detector = poseDetector()
    count = 0
    dir = 0

    while True:
        success, img = cap.read()
        # img = cv2.resize(img, (1280, 720))

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        cv2.putText(img, "Reps Count", (20, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 0), 3)
        if len(lmList) != 0:
            # Right Leg
            angle = detector.findAngle(img, 23, 25, 27)
            # # Left Leg
            # angle = detector.findAngle(img, 24, 26, 28,False)
            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (650, 100))
            # print(angle, per)
            # Check for the knee  bend
            color = (255, 0, 255)

            if angle < 140:
                starttime = time.time()
                cv2.putText(img, "Keep Your knee bent", (225, 600), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)

                if dir == 0 and starttime >= 8:
                    count += 0.5
                    dir = 1
                    starttime = 0

            if angle > 175:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            # print(count)
            # Draw Count
            cv2.putText(img, str(int(count)), (25, 120), cv2.FONT_HERSHEY_PLAIN, 8,
                        (255, 0, 0), 10)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()