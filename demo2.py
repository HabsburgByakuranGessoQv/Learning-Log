from math import cos

from cv2 import cv2
import numpy as np
from numpy import sin


def copy_and_fade(image, padding_size=20):
    h, w, _ = image.shape
    print(type(image))
    print(image.shape)
    print(image)

    # Create a new larger canvas for the expanded image
    expanded_image = np.zeros((h + 2 * padding_size, w + 2 * padding_size, 3), dtype=np.uint8)

    # Copy the original image to the center of the expanded canvas
    expanded_image[padding_size:h+padding_size, padding_size:w+padding_size] = image

    # Copy and fade the border pixels
    for i in range(padding_size):
        alpha = i / padding_size  # Calculate fading alpha value
        # expanded_image[i, padding_size:-padding_size] = (image[0] * alpha + expanded_image[i, padding_size:-padding_size] * (1 - alpha)).astype(np.uint8)
        expanded_image[i, padding_size:-padding_size] = (image[0] * alpha + expanded_image[i, padding_size:-padding_size] * (1 - alpha)).astype(np.uint8)
        expanded_image[-i-1, padding_size:-padding_size] = (image[-1] * alpha + expanded_image[-i-1, padding_size:-padding_size] * (1 - alpha)).astype(np.uint8)
        expanded_image[padding_size:-padding_size, i] = (image[:, 0] * alpha + expanded_image[padding_size:-padding_size, i] * (1 - alpha)).astype(np.uint8)
        expanded_image[padding_size:-padding_size, -i-1] = (image[:, -1] * alpha + expanded_image[padding_size:-padding_size, -i-1] * (1 - alpha)).astype(np.uint8)

    for i in range(padding_size):
        alpha = i / padding_size  # Calculate fading alpha value
        beta = abs(((i - padding_size)^2) / (padding_size^2))
        if beta > 1 :
            beta = 1
        beta = 1 - beta
        beta = round(beta, 2)
        print(beta)

        expanded_image[i, 0:padding_size] = (image[0, 0] * beta + expanded_image[i, 0:padding_size]).astype(np.uint8)
        expanded_image[0:padding_size, i] = (image[0, 0] * beta + expanded_image[0:padding_size, i]).astype(np.uint8)
        # expanded_image[0:padding_size, i] = expanded_image[0:padding_size, i] * alpha
        # expanded_image[i, 0:padding_size] = expanded_image[i, 0:padding_size] * alpha

        expanded_image[i, -padding_size:-1] = (image[0, -1] * beta + expanded_image[i, -padding_size:-1]).astype(np.uint8)
        expanded_image[0:padding_size, -1-i] = (image[0, -1] * beta + expanded_image[0:padding_size, -1-i]).astype(np.uint8)
        # expanded_image[i, -padding_size:-1] = expanded_image[i, -padding_size:-1] * alpha
        # expanded_image[0:padding_size, -1 - i] = expanded_image[0:padding_size, -1-i] * alpha

        expanded_image[-i-1, 0:padding_size] = (image[-1, 0] * beta + expanded_image[-i-1, 0:padding_size]).astype(np.uint8)
        expanded_image[-padding_size:-1, i] = (image[-1, 0] * beta + expanded_image[-padding_size:-1, i]).astype(np.uint8)
        # expanded_image[-i - 1, 0:padding_size] = expanded_image[-i-1, 0:padding_size] * alpha
        # expanded_image[-padding_size:-1, i] = expanded_image[-padding_size:-1, i] * alpha

        expanded_image[-1-i, -padding_size:-1] = (image[-1, 0] * beta + expanded_image[-1-i, -padding_size:-1]).astype(np.uint8)
        expanded_image[-padding_size:-1, -i-1] = (image[-1, 0] * beta + expanded_image[-padding_size:-1, -i-1]).astype(np.uint8)
        # expanded_image[-1 - i, -padding_size:-1] = expanded_image[-1-i, -padding_size:-1] * beta
        # expanded_image[-padding_size:-1, -i - 1] = expanded_image[-padding_size:-1, -i-1] * beta

    return expanded_image


# Load an image
image_path = 'Good/68_540.jpg'  # Replace with your image path
image = cv2.imread(image_path)

# Expand the image
expanded_image = copy_and_fade(image, padding_size=50)

# Display the original and expanded images
cv2.imshow('Original Image', image)
cv2.imshow('Expanded Image', expanded_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
