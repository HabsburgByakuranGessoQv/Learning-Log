import json, os
from PIL import Image

'''
学习使用Python解析标注文件（json文件），读取每棵树冠层的边界点信息；
'''


#json 路径
labelme_jsonpath = r"E:\STUDYCONTENT\Pycharm\Lizhi\labelmefile"
#保存的img路径
save_imgpath = "E:\STUDYCONTENT\Pycharm\Lizhi"

#打开文件
with open(".\labelmefile\labelme_aftercontext.txt", "w+") as f1:
    points_set = [] #保存的是一个三维的列表
    result_points = []  #保存的是一个二维的列表
    for filename in os.listdir(labelme_jsonpath):
        #判断是否为json文件并记录点
        if filename.endswith(".json"):
            #endsWith() 方法用于测试字符串是否以指定的后缀结束。
            #得到一条完整的json文件路径
            json_path = os.path.join(labelme_jsonpath, filename)#.join路径拼接
            #加载出json文件
            json_data = json.load(open(json_path, 'r'))
            #获取数据
            img_name = json_data['imagePath'] #图像名
            for obj in json_data['shapes']:
                if obj['label'] == "tree":
                    points_set.append(obj['points'])
                    for data in obj['points']:  # write() argument must be str, not list
                        result_points.append(data) #存储列表中
                        for unit in data:
                            unit_str = str(unit)
                            if data[0] == unit:
                                f1.write(unit_str+', ')
                            else:
                                f1.write(unit_str+'\n')

            #保存图片
            img = Image.open(os.path.join(labelme_jsonpath, img_name))
            img_save_path = os.path.join(save_imgpath, img_name)
            img.save(img_save_path)
    #print(len(points_set))
    f1.close()


'''
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
            json_path = os.path.join(file_path, filename)  # .join路径拼接
            # 加载出json文件
            json_data = json.load(open(json_path, 'r'))
            # 获取数据
            for obj in json_data['shapes']:
                if obj['label'] == "tree":
                    points_set_ana.append(obj['points'])
    return points_set_ana
'''