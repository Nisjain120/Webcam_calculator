import mediapipe
import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import time

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.value = value
        self.height = height

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 64), cv2.FONT_HERSHEY_COMPLEX, 2, (50, 50, 50), 2)

    def checkclick(self,x,y):
        if(self.pos[0]<x<self.pos[0]+self.width) and (self.pos[1]<y<self.pos[1]+self.height):
            cv2.rectangle(image, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255), cv2.FILLED)
            cv2.rectangle(image, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            cv2.putText(image, self.value, (self.pos[0] + 20, self.pos[1] + 20), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
            return True
        else:
            return False

cap = cv2.VideoCapture(0)
cap.set(3, 1240)
cap.set(4, 640)
detector = HandDetector(detectionCon=0.9, maxHands=1)
delaycounter=0
buttonlistvalue=[['1','2','3','*'],
                ['4','5','6','/'],
                ['7','8','9','+'],
                ['.','0','=','-']]

buttonlist = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y*100 + 150
        buttonlist.append(Button((xpos, ypos), 100, 100, buttonlistvalue[x][y]))
equation=''        

while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    # detection of hands
    hands, image = detector.findHands(image, flipType=False)

    #upar result wla.
    cv2.rectangle(image, (800,50),(800+400,70+100),(225, 225, 225), cv2.FILLED)
    cv2.rectangle(image,(800,50),(800+400,70+100), (50, 50, 50), 3)
    
    # Creation of buttons (within the loop for each button)
    for button in buttonlist:
        button.draw(image)  #function with the image
        
    #check for hands
    if hands:
        lmList = hands[0]['lmList']
        if len(lmList) >= 21:  # Ensure we have at least 21 landmarks
            # Extract x, y coordinates for landmarks 8 and 12
            x1, y1, _ = lmList[8]
            x2, y2, _ = lmList[12]
            
            try:
                length, _, image = detector.findDistance((x1, y1), (x2, y2), image)
                print(length)
            except Exception as e:
                print(f"Error in findDistance: {e}")
            
            x, y, _ = lmList[8]  # Unpack three values, discarding the third
            if length<47 and delaycounter==0:
                for i, button in enumerate(buttonlist):
                    if button.checkclick(x, y):
                        myvalue = buttonlistvalue[int(i/4)][int(i%4)]  # Fixed indexing
                        if myvalue == '=':
                            equation = str(eval(equation))
                        else:
                            equation += myvalue  # Append to equation instead of prepending
                        delaycounter=1   
    if delaycounter!=0:
        delaycounter+=1
        if delaycounter>10:
            delaycounter=0
    #avoid duplicates
    
    #display the equation/result
    cv2.putText(image, equation, (810,130), cv2.FONT_HERSHEY_COMPLEX,1,(50, 50, 50),2)
    
    # Display images
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break
    elif(cv2.waitKey(1)& 0xFF ==ord('c')):
            equation=''

cap.release()
cv2.destroyAllWindows()