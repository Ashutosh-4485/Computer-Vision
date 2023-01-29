import cv2
import mediapipe as mp
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class handDetector():
    def __init__(self,mode=False,maxHands=2,modelComplexity=1,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.modelComplex = modelComplexity
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplex,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB )
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo=0,draw=True):
            lmList=[]
            if self.results.multi_hand_landmarks:
                myHand=self.results.multi_hand_landmarks[handNo]

                for id, lm in enumerate(myHand.landmark):
                    # print(id,lm) #will give u the ratio of the image
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    #print(id, cx, cy)
                    lmList.append([id,cx,cy])
                    # if id==0:
                    if draw:
                        cv2.circle(img, (cx, cy), 3, (255,0,255), cv2.FILLED)
            return lmList



def main():

    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector=handDetector()

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volRange=volume.GetVolumeRange()
    minVol=volRange[0]
    maxVol = volRange[1]
    vol=0
    volBar=400

    while True:
        success, img = cap.read()
        img=detector.findHands(img)
        lmList=detector.findPosition(img)
        if len(lmList)!=0:
           # print(lmList[4], lmList[8])
            #print(lmList[8])
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx,cy=(x1+x2)//2,(y1+y2)//2
            cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (25, 55, 255), 1)
            cv2.circle(img, (cx,cy), 10, (0, 255, 0), cv2.FILLED)

            length=math.hypot(x2-x1,y2-y1)
            #print(length)
           # Hand Range 30 - 300
           # Volume Range -65 - 0
            vol=np.interp(length,[30,300],[minVol,maxVol])
            volBar = np.interp(length, [30, 300], [400,150])
            print(vol)
            volume.SetMasterVolumeLevel(vol, None)

            if length<40:
                cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)

        # cv2.rectangle(img,(50,150),(85,400),(0,0,255),cv2.FILLED)
        # cv2.rectangle(img, (50, int(vol)), (85, 400), (0,0,255),cv2.FILLED)



        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        cv2.imshow('Img', img)
        cv2.waitKey(1)



if __name__=="__main__":
    main()