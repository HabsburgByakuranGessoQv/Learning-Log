import numpy as np
import numpy.fft as fft
import math
from cv2 import cv2 as cv
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

pic = cv.imread('test_img.png')
pic = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)

FA = fft.fft2(pic)  # 对图像进行傅里叶变换
fA = fft.fftshift(FA)  # 对图像频谱进行移动，是0频率点在中心
sA = np.log(np.abs(fA))  # 获得傅里叶变换的幅度谱
phA = np.log(np.angle(fA) * 180 / np.pi)  # 获得傅里叶变换的相位谱

plt.subplot(331), plt.imshow(pic, cmap='gray'), plt.title('原图')
plt.subplot(332), plt.imshow(phA), plt.title('相位谱')
plt.subplot(333), plt.imshow(sA), plt.title('幅度谱')


def highPassFiltering(img, size):  # 传递参数为傅里叶变换后的频谱图和滤波尺寸
    h, w = img.shape[0:2]  # 获取图像属性
    h1, w1 = int(h / 2), int(w / 2)  # 找到傅里叶频谱图的中心点
    img[h1 - int(size / 2):h1 + int(size / 2),
    w1 - int(size / 2):w1 + int(size / 2)] = 0  # 中心点加减滤波尺寸的一半，刚好形成一个定义尺寸的滤波大小，然后设置为0
    return img


def lowPassFiltering(img, size):  # 传递参数为傅里叶变换后的频谱图和滤波尺寸
    h, w = img.shape[0:2]  # 获取图像属性
    h1, w1 = int(h / 2), int(w / 2)  # 找到傅里叶频谱图的中心点
    img2 = np.zeros((h, w), np.uint8)  # 定义空白黑色图像，和傅里叶变换传递的图尺寸一致
    img2[h1 - int(size / 2):h1 + int(size / 2),
    w1 - int(size / 2):w1 + int(size / 2)] = 1  # 中心点加减滤波尺寸的一半，刚好形成一个定义尺寸的滤波大小，然后设置为1，保留低频部分
    img3 = img2 * img  # 将定义的低通滤波与传入的傅里叶频谱图一一对应相乘，得到低通滤波
    return img3


dft_shift = highPassFiltering(fA, 50)
res = np.log(np.abs(dft_shift))
idft_shift = np.fft.ifftshift(dft_shift)  # 将频域从中间移动到左上角
ifimg = np.fft.ifft2(idft_shift)  # 傅里叶库函数调用
ifimg = np.abs(ifimg)
plt.subplot(334), plt.imshow(res), plt.title('高通滤波')
plt.subplot(335), plt.imshow(np.int8(ifimg), 'gray'), plt.title('滤波结果')

fA = fft.fftshift(FA)
plt.subplot(336), plt.imshow(np.int8(fA)), plt.title('频谱')
ldft_shift = lowPassFiltering(fA, 50)
lres = np.log(np.abs(ldft_shift))

# 傅里叶逆变换
lidft_shift = np.fft.ifftshift(ldft_shift)  # 将频域从中间移动到左上角
lifimg = np.fft.ifft2(lidft_shift)  # 傅里叶库函数调用
lifimg = np.abs(lifimg)

plt.subplot(337), plt.imshow(lres), plt.title('低通滤波')
plt.subplot(338), plt.imshow(np.int8(lifimg), 'gray'), plt.title('滤波结果')
plt.show()
