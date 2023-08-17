import os
from cv2 import cv2


def is_image_white(image_path, saturation_threshold=20, brightness_threshold=120):
    # 读取图像
    image = cv2.imread(image_path)

    # 将图像转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算图像的平均亮度
    mean_brightness = gray_image.mean()
    print(f'mean_brightness: {mean_brightness}')

    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 分离H、S、V通道
    h, s, v = cv2.split(hsv_image)

    # 计算图像的平均饱和度
    mean_saturation = s.mean()
    print(f'mean_saturation: {mean_saturation}')

    # 判断图像是否偏白
    if mean_brightness > brightness_threshold and saturation_threshold > mean_saturation:
        return True
    else:
        return False

if __name__ == "__main__":
    image_path = "huai"  # 图像路径
    img_list = os.listdir(image_path)
    for i in range(len(img_list)):
        img_single = os.path.join(image_path, img_list[i])
        print(img_list[i])

        is_white = is_image_white(img_single)
        if is_white:
            print("图像由于摄像头起雾而导致画面部分偏白")
        else:
            print("图像未受摄像头起雾影响，画面正常")