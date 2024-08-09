from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import pyttsx3
import pytesseract
width, height = 1280, 720
gestureThreshold = 300
folderPath = "output_folder"
tesseract_path = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 
cap = cv2.VideoCapture(0)              
cap.set(3, width)
cap.set(4, height)
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(120 * 1), int(213 * 1)  
engine = pyttsx3.init()
engine.setProperty('rate', 150)  

engine.setProperty('rate', 150)   
pytesseract.pytesseract.tesseract_cmd = tesseract_path
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    fixed_size = (800, 600) 
    imgCurrent = cv2.resize(imgCurrent, fixed_size)
    hands, img = detectorHand.findHands(img)  
    if hands and buttonPressed is False:  
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"] 
        fingers = detectorHand.fingersUp(hand) 
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  
            if fingers == [0, 1, 1, 1, 1]:  
                print("Close Presentation")
                buttonPressed = True
                break

            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

            if fingers == [1, 1, 1, 0, 0]: 
                gray_img = cv2.cvtColor(imgCurrent, cv2.COLOR_BGR2GRAY)
                extracted_text = pytesseract.image_to_string(gray_img)
                engine.setProperty('rate', 200) 
                
                engine.say(extracted_text)
                engine.runAndWait()

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:                                                                  
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

        

    else:
        annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    cv2.imshow("Slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()