###
### RECOGNIZER TEST CODE
### DISABLE/ENABLE LED BASED OFF RECOGNIZER DATA
### created by @jmskeoch
### altered from https://iotdesignpro.com/projects/face-recognition-door-lock-system-using-raspberry-pi
###

import cv2
import numpy as np
import os
import RPi.GPIO as GPIO
import time

#RASPI GPIO SETUP
ledPin = 23 # Establish led pin
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Set pinout mode (on a different mode, pin 23 on BCM may be a different number)
GPIO.setup(ledPin, GPIO.OUT) # Set LED pin to output mode 
GPIO.output(ledPin, 1) # Enable LED

#RECOGNIZER SETUP
recognizer = cv2.face.LBPHFaceRecognizer_create() # Initiate recognizer
recognizer.read('trainer.yml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") # Initialize cascade object
font = cv2.FONT_HERSHEY_SIMPLEX
idCount = 0 # Initialize id counter
cam = cv2.VideoCapture(0)
cam.set(3, 640) # Set video width
cam.set(4, 480) # Set video height
minW = 0.1*cam.get(3) # Define minimum window size to be recognized as a face
minH = 0.1*cam.get(4) # "

#ACTIVATE RECOGNIZER SEQUENCE
#print("activating recognizer") --> debugging purposes
while True:
    ret, img = cam.read() # Read camera information
    img = cv2.flip(img, -1) # Flip the image vertically (necessary for cascading)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Set image to grayscale (necessary for cascading)
    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
            )
    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) # Establish a rectangle around face
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w]) # Establish confidence (troubleshooting)
        if(confidence < 100): # Use the confidence level to deactivate LED
            id = names[id]
            confidence = " {0}%".format(round(100 - confidence))
            GPIO.output(ledPin, 0) # Change ledPin output based off confidence result
            print("[INFO] ==> DISABLING LED")
            time.sleep(1)
            GPIO.output(ledPin, 1) # Reset ledPin to enabled state
        else:
            id = "unknown"
            confidence = " {0}%".format(round(100 - confidence))
            GPIO.output(ledPin, 1)
        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
    cv2.imshow('camera', img)
    k = cv2.waitkey(10) & 0xff # Press 'ESC' for exiting video (ESTABLISH CAMERA CONSTANT FOR CLEANUP)
    if k == 27:
        break

#COMPLETE CLEANUP
print("\n [INFO] ==> Exiting Program and Cleaning...")
cam.release()
cv2.destroyAllWindows()
print("\n [INFO] ==> COMPLETE")
