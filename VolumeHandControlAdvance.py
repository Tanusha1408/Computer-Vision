import cv2
import time
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

######################
wCam, hCam = 640, 480
######################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()

    #Find Hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)
    if len(lmList) != 0:

        #Filter based on size
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

        #print(area)
        if 250 < area < 1000:


            #Find distance between index and thumb
            length, img, lineInfo = detector.findDistance(4, 8, img)
            print(length)

        #Convert volume
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        #print(int(length), vol)
        #volume.SetMasterVolumeLevel(vol, None)
        volume.setMasterVolumeLevelScaler(volPer, None)

        #Reduce resolution to make it smoother

        #Check fingers up

        #If pinky is down set volume

        #Drawings

        #Frame rate

        #print(lmList[4], lmList[8])

        #print(length)

        #Hand range 50 - 300
        #Volume range -65 - 0


        if length < 50:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
