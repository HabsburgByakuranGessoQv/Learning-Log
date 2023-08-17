import os
import numpy as np
from cv2 import cv2
import shutil

def add_black_rectangle(image):
    height, width, _ = image.shape
    # top_left = (int(width * 0.1), int(height * 0.1))
    # bottom_right = (int(width * 0.9), int(height * 0.9))
    top_left = (int(width * 0.05), int(height * 0.05))
    bottom_right = (int(width * 0.95), int(height * 0.95))
    color = (0, 0, 0)  # Black color in BGR

    # Add the black rectangle to the image
    modified_image = image.copy()
    cv2.rectangle(modified_image, top_left, bottom_right, color, -1)

    return modified_image


def move_files(source_folder, destination_folder1, destination_folder2):
    for filename in os.listdir(source_folder):
        if filename.endswith('.jpg'):  # 这里可以根据文件类型进行筛选
            source_path = os.path.join(source_folder, filename)

            if should_move_to_folder1(filename):  # 根据条件判断是否移动到文件夹1
                destination_path = os.path.join(destination_folder1, filename)
            else:
                destination_path = os.path.join(destination_folder2, filename)

            shutil.move(source_path, destination_path)


def should_move_to_folder1(filename):
    # 根据您的条件判断是否将文件移动到文件夹1
    # 例如，可以基于文件名、文件大小、文件属性等进行判断
    return True  # 根据条件返回 True 或 False


def calculate_rgb_mean(image_folder):
    rgb_means, image_paths, names = [], [], []

    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg'):
            image_paths.append(os.path.join(image_folder, filename))

    num_img = len(image_paths)
    for index in range(num_img):
        image = cv2.imread(image_paths[index])
        image = add_black_rectangle(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mean = np.mean(image, axis=(0, 1))
        mean = int(mean.mean()) * 20
        rgb_means.append(mean)
        # print(mean)

    return rgb_means

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

if __name__ == '__main__':
    bad_folder = 'Bad'
    good_folder = 'Good'

    create_directory_if_not_exists(bad_folder)
    create_directory_if_not_exists(good_folder)

    image_folder = 'test'

    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg'):
            image_path = os.path.join(image_folder, filename)

            mean_img = cv2.imread(image_path)
            mean_img = add_black_rectangle(mean_img)
            mean_img = cv2.cvtColor(mean_img, cv2.COLOR_BGR2RGB)
            mean = np.mean(mean_img, axis=(0, 1))
            mean = int(mean.mean()) * 20
            # 阈值设置
            if int(mean) <= 400:
                print(f"{filename}: BAD")
                shutil.move(os.path.join(image_folder, filename), bad_folder)
                continue
            else:
                shutil.move(os.path.join(image_folder, filename), good_folder)

