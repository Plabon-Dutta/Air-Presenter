import cv2
import numpy as np
import pyautogui
import sys
import threading
from cvzone.HandTrackingModule import HandDetector
from PyQt5 import QtWidgets
from overlay import Overlay

# Screen and cam config
width, height = 1280, 720
gestureThreshold = 700

cap = cv2.VideoCapture(1)  # Use 1 for external webcam, 0 for default

if not cap.isOpened():
    print("❌ Error: Cannot open webcam!")
    exit()

cap.set(3, width)
cap.set(4, height)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Button & drawing control
buttonPressed = False
delay = 15
counter = 0

annotationStart = False

# Pointer Control
pointer_flag = False

# Setup overlay app
app = QtWidgets.QApplication(sys.argv)
overlay = Overlay()
overlay.show()

# Run overlay in separate thread
threading.Thread(target=app.exec_, daemon=True).start()

# Main loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and not buttonPressed:
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)
        indexFinger = lmList[8][0], lmList[8][1]

        # Gesture zone: top area
        if cy <= gestureThreshold:
            if fingers == [1, 0, 0, 0, 0]:  # Thumb
                print("Previous Slide")
                pyautogui.press('left')
                buttonPressed = True
                pointer_flag = False

            elif fingers == [0, 0, 0, 0, 1]:  # Pinky
                print("Next Slide")
                pyautogui.press('right')
                buttonPressed = True
                pointer_flag = False

        # Pointer mode
        if fingers == [0, 1, 0, 0, 0]:
            print("Pointer Mode")
            if pointer_flag == False:
                pointer_flag = True
                pyautogui.hotkey('ctrl', 'l')
            pyautogui.moveTo(indexFinger[0], indexFinger[1])
            cv2.circle(img, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        # Draw mode
        elif fingers == [0, 1, 1, 0, 0]:
            print("Draw Mode")
            pointer_flag = False
            if not annotationStart:
                overlay.new_stroke()
                annotationStart = True
            overlay.add_point(indexFinger)

        else:
            annotationStart = False

        # Undo
        if fingers == [0, 1, 1, 1, 0]:
            print("Undo")
            pointer_flag = False
            overlay.undo()
            buttonPressed = True

    # Delay after button press
    if buttonPressed:
        counter += 1
        if counter > delay:
            buttonPressed = False
            counter = 0

    # Show camera (debug)
    cv2.imshow("Camera", img)

    if cv2.waitKey(1) == ord('q'):
        break
