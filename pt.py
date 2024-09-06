import cv2
import numpy as np
import mediapipe as mp 
import math


def findAngle (img,p1,p2,p3,lmList,draw = True):
    x1 ,y1 = lmList[p1][1:]#zxy
    x2, y2 = lmList[p2][1:]
    x3, y3 = lmList[p3][1:]
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0: angle +=360
    
    if draw:
        cv2.line(img, (x1,y1), (x2,y2),(0,0,255),3)
        cv2.line(img, (x3,y3), (x2,y2),(0,0,255),3)
        
        cv2.circle(img, (x1,y1), 5,(255,255,00))
        cv2.circle(img, (x2,y2), 5,(255,255,00))
        cv2.circle(img, (x3,y3), 5,(255,255,00))
        
        cv2.circle(img, (x1,y1), 2,(255,255,00),cv2.FILLED)
        cv2.circle(img, (x2,y2), 2,(255,255,00),cv2.FILLED)
        cv2.circle(img, (x3,y3), 2,(255,255,00),cv2.FILLED)


        
        cv2.putText(img,str(int(angle)),(x2-40,y2-40), cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255))
        
    return angle
        

dir = 0
count = 0


mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture("video2.mp4")

while True:
    succes,img = cap.read()
    if not succes:
        break
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    results = pose.process(imgRGB)
    lmList = []
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    
        for id ,lm in enumerate(results.pose_landmarks.landmark):
            h ,w ,_ = img.shape
            
            cx, cy = int(lm.x*w),int(lm.y*h)
            
            lmList.append([id,cx,cy])
            
    if lmList != 0:
        angle = findAngle(img, 23, 25, 27, lmList)
        per = np.interp(angle,(80,145),(0,100))
        
        print(count)
        
        if per == 100:
            if dir == 0:
                count+=0.5
                dir =1
        if per == 0:
            if dir == 1:
                count+=0.5
                dir =0
    
    cv2.putText(img, str(int(count)),(50,50), cv2.FONT_HERSHEY_TRIPLEX,2,(0,255,255))
    cv2.imshow("img",img)
    k = cv2.waitKey(100) & 0xFF
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()

cv2.destroyAllWindows()