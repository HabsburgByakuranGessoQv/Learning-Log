import os
import matplotlib.pyplot as plt
import cv2.cv2 as cv2
import numpy as np

# https://www.cnblogs.com/goushibao/p/6671079.html
# https://blog.csdn.net/qq_35189715/article/details/95937151

'''
cv2.IMREAD_COLOR：默认参数，读入一副彩色图片，忽略alpha通道 cv2.IMREAD_GRAYSCALE：读入灰度图片
cv2.IMREAD_UNCHANGED：顾名思义，读入完整图片，包括alpha通道
'''
# 存放各类拼接图的路径
# Splice_file = r'E:\STUDYCONTENT\Pycharm\Lizhi\SplicedImage'
Splice_file = r'E:\STUDYCONTENT\Pycharm\Lizhi'
# 遍历所有该文件夹下的文件
for filename in os.listdir(Splice_file):
    # 判断是否为.tif为后缀的文件
    if filename.endswith('.tif'):
        img = cv2.imread('{0}\{1}'.format(Splice_file, filename), -1)
        print('{0} shape:'.format(filename), img.shape)
        print('{0} dtype:'.format(filename), img.dtype)
        print('{0} max:'.format(filename), np.nanmax(img))
        print('{0} min:'.format(filename), np.nanmin(img))
        print('{0} mean:'.format(filename), np.nanmean(img))
        # cv2.imshow('{0}'.format(filename), img)
        plt.matshow(img)
        plt.show()
    if filename.endswith('.jpg'):
        img = cv2.imread('{0}\{1}'.format(Splice_file, filename))
        print('{0} shape:'.format(filename), img.shape)
        print('{0} dtype:'.format(filename), img.dtype)
        print('{0} max:'.format(filename), np.nanmax(img))
        print('{0} min:'.format(filename), np.nanmin(img))
        print('{0} mean:'.format(filename), np.nanmean(img))
        # plt.matshow(img)
        # plt.show()
        # cv2.imshow('{0}'.format(filename), img)
        # 预览黑屏

# cv2.waitKey(0)
# cv2.destroyWindow()
