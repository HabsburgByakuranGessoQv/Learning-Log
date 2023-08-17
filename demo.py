from cv2 import cv2
import numpy as np
import time
import  PoseModule as pm

cap = cv2.VideoCapture(r'E:/STUDYCONTENT/Pycharm/PoseEstimation/Data/2022-05-23 23-49-29.mp4')
detector = pm.poseDetector()

while True:
    success, img = cap.read()

    # img = cv2.imread(r'E:/STUDYCONTENT/Pycharm/PoseEstimation/Data/2022-05-23 23-49-29.mp4')
    # img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img)

    cv2.imshow('image', img)
    cv2.waitKey(1)