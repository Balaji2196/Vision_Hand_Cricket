import cv2
import mediapipe as mp
import time
import os
import numpy as np
import random

cap=cv2.VideoCapture(0)


folderPath='FingerImages'
path=os.getcwd()
path=os.path.join(path,'FingerImages')

myList=os.listdir(path)
myList.sort()
print(myList)

overLayList=[]
for impath in myList:
    image=cv2.imread(os.path.join(path,impath))
    image=cv2.resize(image,(200,200))
    overLayList.append(image)


mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
check=0
score=0
pTime=0
cTime=0
count=0
prev_count=0
tipIds=[4,8,12,16,20]
frame_count=0
while True:
    suc,img=cap.read()
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,'FPS:{}'.format(int(fps)),(250,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    lmList=[]
    if results.multi_hand_landmarks:
            myHand=results.multi_hand_landmarks[0]
            for id,lm in enumerate(myHand.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                lmList.append([id,cx,cy])
                mpDraw.draw_landmarks(img,myHand,mpHands.HAND_CONNECTIONS)
                cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
    if len(lmList) !=0:            
        #print(len(lmList))
        fingers=[]
        #Thumb
        if lmList[tipIds[0]][1]<lmList[tipIds[0]-1][1]:
            fingers.append(0)
        else:
            fingers.append(1)
            
        for id in range(1,5): 
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        count=fingers.count(1)
        
        if ((lmList[tipIds[0]][2]<lmList[tipIds[1]][2]) and (lmList[tipIds[0]][2]<lmList[tipIds[2]][2]) and (lmList[tipIds[0]][2]<lmList[tipIds[3]][2]) and (lmList[tipIds[0]][2]<lmList[tipIds[4]][2])):
            count=6
        if count==prev_count:
            frame_count+=1
            if frame_count==10:
                height,width,channel=overLayList[0].shape
                check=random.randint(1,6)
                if check == count:
                    print(check,count)
                    print("GAME OVER")
                    print("COMPUTER ALSO GENERATED {}".format(check))
                    time.sleep(1)
                    img[0:200,440:640]=overLayList[check-1]
                    img[0:200,0:200]=overLayList[count-1]
                    cv2.putText(img,"Your Score:{}".format(score),(175,250),cv2.FONT_HERSHEY_PLAIN,2,(255,255,0),3)
                    cv2.putText(img,"GAME OVER".format(count),(240,150),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),3)
                    cv2.putText(img,"Player:{}".format(count),(0,250),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3)
                    cv2.putText(img,"Computer:{}".format(check),(440,250),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3)
                    cv2.imshow("image",img)
                    cv2.waitKey(10000)
                    break
                else:
                    score+=count
                    #print(check,count)
                    print("score: ",score)
                frame_count=0
                
        else:
            frame_count=0
        prev_count=count
    img[0:200,0:200]=overLayList[count-1]
    img[0:200,440:640]=overLayList[check-1]
    cv2.putText(img,"Player:{}".format(count),(0,250),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3)
    cv2.putText(img,"Computer:{}".format(check),(440,250),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3)
    cv2.putText(img,"Score:{}".format(score),(240,250),cv2.FONT_HERSHEY_PLAIN,2,(255,255,0),3)
    #print("score: ",score)
    cv2.imshow("image",img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
print("final_score:",score)
cap.release()
cv2.destroyAllWindows()
