from cv2 import cv2
import mediapipe as mp
import numpy as np
import time
import math


class poseDetector:
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, 1, self.upBody, False, self.smooth,
                                     self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):
        # img = cv2.imread(img)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        # 获取坐标
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        # 计算角度
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        # print(angle)
        # 在图中画出来
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 255, 0), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 255, 0), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 255, 0), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        return angle


def main():
    cap = cv2.VideoCapture(r'E:\STUDYCONTENT\Pycharm\PoseEstimation\Data\bl.mp4')
    pTime = 0
    fwc_dir, qwt_dir = 0, 0
    fwc_count, qwt_count = 0, 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        # img = cv2.imread(r'E:\STUDYCONTENT\Pycharm\PoseEstimation\Data\2022-05-23 23-52-23.mp4')
        # img = cv2.resize(img, (1280, 720))
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            # 计算角度 进度
            fwc_angle, qwt_angle = detector.findAngle(img, 12, 14, 16, False), detector.findAngle(img, 14, 12, 26, True)
            fwc_per, qwt_per = np.interp(fwc_angle, (55, 170), (0, 100)), np.interp(qwt_angle, (215, 330), (0, 100))
            print(qwt_angle, qwt_per)

            # 检查进度
            if fwc_per == 100:
                if fwc_dir == 0:
                    fwc_count += 0.5
                    fwc_dir = 1
            if fwc_per == 0:
                if fwc_dir == 1:
                    fwc_count += 0.5
                    fwc_dir = 0
            if qwt_per == 100:
                if qwt_dir == 0:
                    qwt_count += 0.5
                    qwt_dir = 1
            if qwt_per == 0:
                if qwt_dir == 1:
                    qwt_count += 0.5
                    qwt_dir = 0

        # 计数显示
        cv2.putText(img, 'FWC:' + str(int(fwc_count)), (100, 600), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
        cv2.putText(img, 'QWT:' + str(int(qwt_count)), (100, 500), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)

        # fps 计算
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, 'FPS:' + str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
