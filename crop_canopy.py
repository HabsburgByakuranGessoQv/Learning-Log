import json

import cv2.cv2 as cv2
# from utils import get_mask_bounding, json_to_dict
import numpy as np
from os.path import join, basename
from os import listdir, makedirs

ori_dir = r'E:\STUDYCONTENT\Pycharm\Lizhi\labelmefile'
tgt_dir = r'E:\STUDYCONTENT\Pycharm\Lizhi\demo'

mask_flag = True


def get_mask_bounding(mask: np.ndarray):
    x_min = np.min(mask[:, 0])
    x_max = np.max(mask[:, 0])
    y_min = np.min(mask[:, 1])
    y_max = np.max(mask[:, 1])
    return np.array([[x_min, y_min, x_max, y_max]])


def json_to_dict(json_path):
    with open(json_path) as o:
        content = o.read()
    d = json.loads(content)
    return d


def crop_img(img_path: str):
    date = img_path.split('_')[0]
    ano_path = img_path.split('.')[0] + '.json'
    img = cv2.imread(join(ori_dir, img_path), -1)
    h, w = img.shape[:2]
    ano = json_to_dict(join(ori_dir, ano_path))
    shapes = ano['shapes']
    for i in range(len(shapes)):
        output_path = '{}_{}'.format(i, date)
        points = np.array(shapes[i]['points'], dtype=int)
        x_min, y_min, x_max, y_max = get_mask_bounding(points)[0]
        if x_min < 0 or y_min < 0 or x_max >= w or y_max >= h:
            ins_img = np.zeros(shape=[1, 1, 3], dtype=np.uint8)
            cv2.imwrite(join(tgt_dir, output_path), ins_img)
            continue

        ins_img = img[y_min:y_max, x_min:x_max]
        if not mask_flag:
            cv2.imwrite(join(tgt_dir, output_path), ins_img)
            continue
        points[:, 0] -= x_min
        points[:, 1] -= y_min

        mask = np.zeros(ins_img.shape[:2], np.uint8)
        points = np.array([points], dtype=int)
        mask1 = cv2.polylines(mask, points, 1, 255)
        mask2 = cv2.fillPoly(mask, points, 255)
        dst = cv2.bitwise_and(ins_img, ins_img, mask=mask2)

        cv2.imwrite(join(tgt_dir, output_path), dst)


if __name__ == '__main__':
    file_ls = [f for f in listdir(ori_dir) if 'tif' in f]
    for f in file_ls:
        print(f)
        crop_img(f)
