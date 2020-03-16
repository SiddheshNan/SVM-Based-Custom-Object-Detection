# USAGE
# python test_detector.py --detector face_detector/detector.svm --testing face_detector/testing

# import the necessary packages
# from __future__ import print_function
import dlib
import paho.mqtt.client as paho
import cv2
import numpy as np
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS

webcam = cv2.VideoCapture(1)

face_cascade = cv2.CascadeClassifier('face.svm')
# load the detector
detector1 = dlib.simple_object_detector('model/car_detector2.svm')
detector2 = dlib.simple_object_detector('model/b1_detector.svm')
detector4 = dlib.simple_object_detector('model/auto_detector.svm')

# loop over the testing images
while True:
    # for testingPath in paths.list_images(args["testing"]):
    # load the image and make predictions
    _, image = webcam.read()
    image = imutils.resize(image, width=400)
    orig = image.copy()
    bgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(bgray)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, 'face detected', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
    else:
        nimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes1 = detector1(nimage)
        boxes2 = detector2(nimage)
        boxes4 = detector4(nimage)
        for b in boxes1:
            (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
            cv2.rectangle(orig, (x, y), (w, h), (0, 255, 0), 2)
            cv2.putText(image, 'car detected', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
        for b in boxes2:
            (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
            cv2.rectangle(orig, (x, y), (w, h), (0, 255, 0), 2)
            cv2.putText(image, 'bike detected', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)

        for b in boxes4:
            (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
            cv2.rectangle(orig, (x, y), (w, h), (0, 255, 0), 2)
            cv2.putText(image, 'auto detected', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)

    cv2.imshow("Image", np.hstack([image]))
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
# cv2.waitKey(0)
