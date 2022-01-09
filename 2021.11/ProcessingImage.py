import json
import os
import cv2.cv2 as cv2
import numpy as np


def analysis_tree(file_path):
    points_set_ana = []  # 保存的是一个三维的列表
    for filename in os.listdir(file_path):
        # 判断是否为json文件并记录点
        if filename.endswith(".json"):
            # endsWith() 方法用于测试字符串是否以指定的后缀结束。
            # 得到一条完整的json文件路径
            json_path_ana = os.path.join(file_path, filename)  # .join路径拼接
            # 加载出json文件
            json_data = json.load(open(json_path_ana, 'r'))
            # 获取数据
            for obj in json_data['shapes']:
                if obj['label'] == "tree":
                    points_set_ana.append(obj['points'])
    return points_set_ana


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


if __name__ == '__main__':
    save_Tpa1 = r".\tree"
    img_path = r'.\SplicedImage'

    # json 路径
    json_path = r".\labelmefile"
    # 获取坐标
    points_set = analysis_tree(json_path)

    for fileName in os.listdir(img_path):
        if fileName.endswith(".tif"):
            # 得到前缀名
            frontName = fileName.split('.')[0]
            # 读取文件
            img_ini = cv2.imread(os.path.join(img_path, fileName), -1)
            # 创建保存文件夹路径
            savePath = os.path.join(save_Tpa1, frontName)
            # 创建文件夹存放切割图片
            isExist = os.path.exists(savePath)
            if not isExist:
                os.makedirs(savePath)
                print('&-*'*10 + frontName + '文件夹创建成功！' + '&-*'*10)
            else:
                print('&-*'*10 + frontName + '文件夹已经存在' + '&-*'*10)
            numName = 0
            for i in points_set:
                numName += 1
                # 创建保存的文件名
                saveName = '{0}_{1}.tif'.format(frontName, numName)
                print(saveName)
                if img_ini is not None:
                    img_data = Matting(img_ini, i)
                    print('&-*'*10 + 'LOADING' + '&-*'*10)
                    cv2.imwrite(os.path.join(savePath, saveName), img_data)
                    print('Success! ' + saveName)
                else:
                    print('IMG IS NONE')
