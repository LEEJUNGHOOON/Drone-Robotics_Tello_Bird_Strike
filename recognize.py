import cv2
import numpy as np


cap = cv2.VideoCapture('udp://0.0.0.0:11111')
birds_cascade = cv2.CascadeClassifier("./python-tello-bird-detection/birds1.xml")
while True:
    # Get webcam images
    ret, frame = cap.read()

    # convert the frame into gray scale for better analysis
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect birds in the gray scale image
    birds = birds_cascade.detectMultiScale(
        gray,
        scaleFactor=1.4,
        minNeighbors=5,
        #minSize=(10, 10),
        maxSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    if (len(birds)>=3):
        print("Detected {0} Birds".format(len(birds)))

    # Draw a rectangle around the detected birds approaching the farm
    for (x, y, w, h) in birds:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 0), 2)

    # Display the resulting frame
    print(frame)
    cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()
