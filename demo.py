from cv2 import cv2
import numpy as np

def pad_with_border_copy(image, padding_size):
    h, w = image.shape[:2]

    padded_image = np.zeros((h + 2 * padding_size, w + 2 * padding_size, 3), dtype=np.uint8)
    padded_image[padding_size:h+padding_size, padding_size:w+padding_size] = image

    # Copy border pixels
    padded_image[:padding_size, padding_size:w+padding_size] = image[0]  # Top border
    padded_image[h+padding_size:, padding_size:w+padding_size] = image[h-1]  # Bottom border
    padded_image[padding_size:h+padding_size, :padding_size] = image[:, 0].reshape(-1, 1, 3)  # Left border
    padded_image[padding_size:h+padding_size, w+padding_size:] = image[:, w-1].reshape(-1, 1, 3)  # Right border

    # Copy corner pixels
    padded_image[:padding_size, :padding_size] = image[0, 0]  # Top-left corner
    padded_image[:padding_size, w+padding_size:] = image[0, -1]  # Top-right corner
    padded_image[h+padding_size:, :padding_size] = image[-1, 0]  # Bottom-left corner
    padded_image[h+padding_size:, w+padding_size:] = image[-1, -1]  # Bottom-right corner

    return padded_image


def mid_map(img, pad_img, back_img, x, y, pad_size):
    h, w = img.shape[:2]
    for i in range(pad_size):
        alp = i / pad_size
        back_alp = 1 - alp
        # print(back_alp)

        # pad_img[i, pad_size:pad_size+w] = pad_img[i, pad_size:pad_size+w] + (back_img[y+i, x+pad_size:x+pad_size+w]) * back_alp

        # pad_img[i, pad_size:pad_size+w] = pad_img[i, pad_size:pad_size+w] * alp + (back_img[y, x+pad_size:x+pad_size+w]) * back_alp
        # pad_img[i+h+pad_size, pad_size:pad_size+w] = pad_img[i+h+pad_size, pad_size:pad_size+w] * back_alp + ((back_img[y+h+(2*pad_size), x+pad_size:x+pad_size+w]) * alp)
        # pad_img[pad_size:pad_size+h, i] = pad_img[pad_size:pad_size+h, i] * alp + ((back_img[y+pad_size:y+pad_size+h, x]) * back_alp)
        # pad_img[pad_size:pad_size+h, -i] = pad_img[pad_size:pad_size+h, -i] * alp + ((back_img[y+pad_size:y+pad_size+h, x+w+2*pad_size]) * back_alp)

        pad_img[i, :] = pad_img[i, :] * alp + (back_img[y, x:x+2*pad_size+w]) * back_alp
        pad_img[i+h+pad_size, :] = pad_img[i+h+pad_size, :] * back_alp + ((back_img[y+h+(2*pad_size), x:x+2*pad_size+w]) * alp)
        pad_img[:, i] = pad_img[:, i] * alp + ((back_img[y:y+2*pad_size+h, x]) * back_alp)
        pad_img[:, -i] = pad_img[:, -i] * alp + ((back_img[y:y+2*pad_size+h, x+w+2*pad_size]) * back_alp)

        # pad_img[:i, :i] = image[0, 0] * alp + back_img[y, x] * back_alp  # Top-left corner
        # pad_img[:pad_size, w + pad_size:] = image[0, -1]  # Top-right corner
        # pad_img[h + pad_size:, :pad_size] = image[-1, 0]  # Bottom-left corner
        # pad_img[h + pad_size:, w + pad_size:] = image[-1, -1]  # Bottom-right corner



    return pad_img

# Load an image
# image_path = 'Good/68_540.jpg'
# image_path = 'Good/82_660.jpg'
# image_path = 'Good/83_560.jpg'
image_path = 'Good/88_760.jpg'
# image_path = 'houzi.png'
image = cv2.imread(image_path)
img_h, img_w = image.shape[:2]

background_path = r'Good/background.jpg'
background = cv2.imread(background_path)

# Specify padding size
padding_size = 30

# 指定嵌入位置的坐标 (x, y)
x, y = 100, 150
kernel_size = (11, 11)

# 改变亮度
# 指定区域的左上角和右下角坐标
# 指定范围的左上角和右下角坐标
x1, y1 = x - kernel_size[0], y - kernel_size[1] # 左上角坐标
x2, y2 = x1 + 2 * padding_size + img_w + 2 * kernel_size[0], y1 + 2 * padding_size + img_h + 2 * kernel_size[1]  # 右下角坐标

# 提取指定区域
region_of_interest = background[y1:y2, x1:x2]

# # 计算区域的平均亮度值
# average_brightness = np.mean(cv2.cvtColor(region_of_interest, cv2.COLOR_BGR2GRAY))
#
# # 将整幅图像的亮度值进行调整，以匹配平均亮度
# image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# adjusted_image = np.clip(image_gray + (average_brightness - np.mean(image_gray)), 0, 255)
########

# 计算区域的平均亮度值
average_brightness = np.mean(cv2.cvtColor(region_of_interest, cv2.COLOR_BGR2GRAY))

# 获取整个图像的每个通道
b, g, r = cv2.split(image)

# 计算每个通道的亮度调整值
adjustment_b = average_brightness - np.mean(b)
adjustment_g = average_brightness - np.mean(g)
adjustment_r = average_brightness - np.mean(r)

# 对各个通道进行亮度调整
adjusted_b = np.clip(b + adjustment_b, 0, 255)
adjusted_g = np.clip(g + adjustment_g, 0, 255)
adjusted_r = np.clip(r + adjustment_r, 0, 255)

# 合并调整后的通道
adjusted_image = cv2.merge((adjusted_b, adjusted_g, adjusted_r))

#############
#
# # 转换为彩色图像
# adjusted_image = cv2.cvtColor(adjusted_image.astype(np.uint8), cv2.COLOR_GRAY2BGR)



# Pad with border and corner copy
# padded_image = pad_with_border_copy(adjusted_image, padding_size)
padded_image = pad_with_border_copy(image, padding_size)
padded_image = mid_map(image, padded_image, background, x, y, padding_size)
# padded_image = mid_map(adjusted_image, padded_image, background, x, y, padding_size)



# 应用高斯模糊
blurred_upper = cv2.GaussianBlur(padded_image, kernel_size, sigmaX=0)



# Display the original and padded images
cv2.imshow('Original Image', image)
cv2.imshow('upper', padded_image)
cv2.imshow('adjust', adjusted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


def embed_image(background, foreground, x, y):
    h, w = foreground.shape[:2]
    background[y:y+h, x:x+w] = foreground
    return background


# Load the background and foreground images
foreground = blurred_upper

# 指定融合权重
alpha = 1  # 调整此值以获得所需的融合效果

# 图像融合操作
blended_image = cv2.addWeighted(background[y:y+foreground.shape[0], x:x+foreground.shape[1]], 1-alpha,
                                foreground, alpha, 0)

# 将融合图像放回目标图片的指定位置
background[y:y+blended_image.shape[0], x:x+blended_image.shape[1]] = blended_image

# 背景再模糊
# 提取指定范围的图像区域
region_of_interest = background[y1:y2, x1:x2]

kernel_size_back = (11, 11)

# 混合原始图像和模糊后的区域
blurred_back = cv2.GaussianBlur(region_of_interest, kernel_size_back, sigmaX=0)
# 将模糊后的区域放回原图像
background[y1:y2, x1:x2] = blurred_back




# Embed the foreground image into the background at the specified position
result_image = embed_image(background.copy(), image, x+padding_size, y+padding_size)
# result_image = embed_image(background.copy(), adjusted_image, x+padding_size, y+padding_size)



# Display the result
cv2.namedWindow('Embedded Image', cv2.WINDOW_NORMAL)
cv2.imshow('Embedded Image', result_image)
cv2.waitKey(0)
