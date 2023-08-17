import cv2.cv2 as cv2
import numpy as np


def Matting(img, Coordinate_set):
    points_set_Ma = np.array(Coordinate_set, dtype=int)  # 多边形的顶点集
    # 坐标获取
    col0 = points_set_Ma[:, 0]
    col1 = points_set_Ma[:, 1]
    x1 = np.min(col0)
    y1 = np.min(col1)
    x2 = np.max(col0)
    y2 = np.max(col1)

    single_tree = img[y1:y2, x1:x2]  # 对大图进行初次切割，得到一个包含该树的小图
    # 对坐标进行再次操作，使坐标对应于新的小图
    points_set_Ma[:, 0] -= x1
    points_set_Ma[:, 1] -= y1
    points_final = np.array([points_set_Ma], dtype=int)

    # 将坐标刻画在坐标板上
    Cp = np.zeros(single_tree.shape[:2], np.uint8)  # 获得一个与该图片有同样大小但是里面数据用0填充的数组
    Cpm = cv2.polylines(Cp, points_final, True, 255)  # 打点
    Cpf = cv2.fillPoly(Cpm, points_final, 255)
    img_tree = cv2.bitwise_and(single_tree, single_tree, mask=Cpf)
    # 作图
    # 扣出来的图的数据所形成的图片
    return img_tree
