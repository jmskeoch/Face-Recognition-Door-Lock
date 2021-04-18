#DATA GATHERING FOR FACIAL RECOGNITION SPRING FINAL PROIJECT
#SOURCE: https://iotdesignpro.com/projects/face-recognition-door-lock-system-using-raspberry-pi
import cv2
import os
import pkg_resources

cam = cv2.VideoCapture(0)
cam.set(3, 640) #WIDTH
cam.set(4, 480) #HEIGHT

#Initialize the face detector
haar_xml = pkg_resources.resource_filename('cv2', 'data/haarcascade_Frontalface_default.xml')
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#Numeric Face ID Input
face_id = input('\n ENTER USER ID ==>  ')
print("\n [INFO] Initializing face capture. Look towards camera...")
#Face Sampling Count
count = 0

while(True):
	ret, img = cam.read()
	img = cv2.flip(img, -1) #FLIP VERTICALLY
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_detector.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
	k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
	if k == 27:
		break
	elif count >= 30: # Take 30 face sample and stop video
		break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

