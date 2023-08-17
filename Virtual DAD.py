import cv2.cv2 as cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 打开摄像头
cap.set(3, 1280)  # 设置视频宽度
cap.set(4, 720)  # 设置视频高度
detector = HandDetector(detectionCon=0.8, maxHands=2)  # 初始化识别器 设置精度

colorD = 100, 50, 255
cx, cy, w, h = 100, 100, 200, 200


class DragGraph:
    def __init__(self, pos_cen, size=[150, 150], color=(100, 50, 255)):
        self.pos_cen = pos_cen
        self.size = size
        self.color = color

    def update(self, cursor):
        cx, cy = self.pos_cen
        w, h = self.size
        # If th index finger tip is the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.color = 0, 255, 0
            self.pos_cen = cursor


rectList = []
for i in range(4):
    rectList.append(DragGraph([i * 250 + 150, 150]))

while 1:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # 翻转画面
    # draw the outline
    # hands, img = detector.findHands(img, flipType=False)
    # not draw the outline
    hands = detector.findHands(img, draw=False, flipType=False)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right
        if lmList1:
            # draw the line
            # twoFin, _, _ = detector.findDistance(lmList1[8], lmList1[12], img)
            # cleanFin, _, _ = detector.findDistance(lmList1[8], lmList1[20], img)
            # bigFin, _, _ = detector.findDistance(lmList1[8], lmList1[4], img)
            # not draw the line
            twoFin, _ = detector.findDistance(lmList1[8], lmList1[12])
            cleanFin, _ = detector.findDistance(lmList1[8], lmList1[20])
            bigFin, _ = detector.findDistance(lmList1[8], lmList1[4])
            if twoFin < 50:
                cursor = lmList1[8]  # index finger tip landmark
                # call the update
                for rect in rectList:
                    rect.update(cursor)
            else:
                for rect in rectList:
                    rect.color = colorD
            if bigFin < 30 and cleanFin > 300:
                print("Rebuilding!")
                for i in range(4):
                    rectList.append(DragGraph([i * 250 + 150, 150]))
            if cleanFin < 30:
                print("Clean!")
                for rect in rectList:
                    rectList.pop()

    # Draw solid
    # for rect in rectList:
    #     cx, cy = rect.pos_cen
    #     w, h = rect.size
    #     cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)
    #     cvzone.cornerect(img, (cx-w//2, cy-h//2, w, h), 20, rt=0)

    #  Draw Transparency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.pos_cen
        w, h = rect.size
        colorNew = rect.color
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorNew, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.1
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Capture", out)
    if cv2.waitKey(30) == 27:  # esc to quit program
        break
