import cv2
import numpy as np
import time
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam=640,480


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(3,hCam)
pTime=0;
cTime=0

detector=htm.handDetector(detectionCon=0.7)


devices= AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
#volume.setMasterVolumeLevel(-20.0,None)


while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        #print(lmList[4], lmList[8])
        print(lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cv2.circle(img,(x1,y1),35,(255,255,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 30, (255, 255, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,255),2)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'FPS:{int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.imshow("Camera",img)
    cv2.waitKey(1)
