# 导入包
import numpy as np
from cv2 import cv2

# 读取，显示图像
# raw_img = cv2.resize(cv2.imread('test_img.png', 1), (300, 300))
raw_img = cv2.imread('test_img.png', 1)
cv2.imshow('raw_img', raw_img)
# cv2.waitKey(0)

# 图片格式转换
gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)

cv2.imshow('gray_img', gray_img)

# 灰度变化
# 对灰度图像进行对比度拉伸
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_img)
dst_img = cv2.convertScaleAbs(gray_img, alpha=255.0 / (max_val - min_val), beta=-min_val * 255.0 / (max_val - min_val))

canvas = np.zeros((gray_img.shape[0], gray_img.shape[1]*2), dtype=np.uint8)
canvas[:, :gray_img.shape[1]] = gray_img
canvas[:, gray_img.shape[1]:] = dst_img
cv2.imshow('Grayscale Conversion', canvas)

# 图片模糊
# 使用均值滤波器对图像进行模糊处理
blur_img = cv2.blur(raw_img, (5, 5))

# 在同一个窗口中显示原始图像和模糊后的图像
canvas = np.zeros((raw_img.shape[0], raw_img.shape[1]*2, 3), dtype=np.uint8)
canvas[:, :raw_img.shape[1], :] = raw_img
canvas[:, raw_img.shape[1]:, :] = blur_img
cv2.imshow('Image Blurring', canvas)

# 图像直方图均衡化
equ_img = cv2.equalizeHist(gray_img)
# 在同一个窗口中显示原始图像和直方图均衡化后的图像
canvas = np.zeros((raw_img.shape[0], raw_img.shape[1]*2), dtype=np.uint8)
canvas[:, :raw_img.shape[1]] = gray_img
canvas[:, raw_img.shape[1]:] = equ_img
cv2.imshow('Histogram Equalization', canvas)

cv2.waitKey(0)
