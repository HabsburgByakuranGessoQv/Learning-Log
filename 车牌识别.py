from cv2 import cv2
import numpy as np

# # 读取图像
# img = cv2.imread('pure.jpeg', cv2.IMREAD_GRAYSCALE)
# # 定义结构元素
# kernel = np.ones((3,3), np.uint8)
# # 膨胀操作
# dilation = cv2.dilate(img, kernel, iterations=1)
# # 腐蚀操作
# erosion = cv2.erode(img, kernel, iterations=1)
# # 边缘检测
# edges = cv2.absdiff(dilation, erosion)
# # 显示图像
# cv2.imshow('Original', img)
# cv2.imshow('Edges', edges)
# # cv2.waitKey(0)
# cv2.destroyAllWindows()
# # 定义结构元素
# kernel = np.ones((5,5), np.uint8)
# # 开运算
# opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
# # 闭运算
# closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
# # 显示图像
# #cv2.imshow('Original', img)
# cv2.imshow('Opening', opening)
# cv2.imshow('Closing', closing)
# #cv2.waitKey(0)
# cv2.destroyAllWindows()

img = cv2.imread('pure.jpeg')#, cv2.IMREAD_GRAYSCALE)
# 灰度化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 二值化
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
# 形态学操作
kernel = np.ones((5,5), np.uint8)
kernel2 = np.ones((7,7), np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2)
#cv2.imshow('closing', closing)
opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
# 查找轮廓
contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
#mask=cv2.drawContours(img,contours,0,255,cv2.FILLED)

# 寻找最大的轮廓
max_contour = max(contours, key=cv2.contourArea)
# 绘制轮廓
cv2.drawContours(img, [max_contour], 0, (0,255,0), 3)
# 显示图像
cv2.imshow('Original', img)
cv2.imshow('Thresh', thresh)
cv2.imshow('Opening', opening)
cv2.waitKey(0)
cv2.destroyAllWindows()
# 获取车牌区域的坐标
x, y, w, h = cv2.boundingRect(max_contour)
# 裁剪车牌区域
plate_img = img[y:y+h, x:x+w]
# 灰度化
gray_plate = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
# 二值化
ret, thresh_plate = cv2.threshold(gray_plate, 127, 255, cv2.THRESH_BINARY)
# 形态学操作
kernel_plate = np.ones((4,4), np.uint8)
closing_plate = cv2.morphologyEx(thresh_plate, cv2.MORPH_CLOSE, kernel_plate)
# 查找轮廓
contours_plate, hierarchy_plate = cv2.findContours(closing_plate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 遍历轮廓
for contour in contours_plate:
    # 获取轮廓区域的坐标
    x_c, y_c, w_c, h_c = cv2.boundingRect(contour)
    # 过滤掉小块区域
    if w_c * h_c > 2000:
        # 绘制区域
        cv2.rectangle(plate_img, (x_c, y_c), (x_c+w_c, y_c+h_c), (0, 255, 0), 2)
# 显示图像
cv2.imshow('Original', img)
cv2.imshow('Plate', plate_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
