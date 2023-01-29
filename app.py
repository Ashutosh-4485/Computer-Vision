import cv2
import numpy as np
import time
import PoseModule as pm



cap = cv2.VideoCapture("KneeBendVideo.mp4")

detector = pm.poseDetector()
count = 0
dir = 0

while True:
    success, img = cap.read()
    #img = cv2.resize(img, (1280, 720))

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
            cv2.putText(img,"Keep Your knee bent", (225, 600), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)

            if dir == 0 and starttime>=8:
                count += 0.5
                dir = 1
                starttime=0

        if angle > 175:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        #print(count)
        # Draw Count
        cv2.putText(img, str(int(count)), (25,120), cv2.FONT_HERSHEY_PLAIN, 8,
                    (255, 0, 0), 10)


    cv2.imshow("Image", img)
    cv2.waitKey(1)