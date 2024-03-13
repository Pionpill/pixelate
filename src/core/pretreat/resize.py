import math

import numpy as np
from PIL import Image


def resize(image: np.ndarray, options: dict) -> np.ndarray:
    ori_image = Image.fromarray(image)
    nonzero_pixels = ori_image.getbbox()

    # 计算最小外接矩形的宽度和高度
    width = nonzero_pixels[2] - nonzero_pixels[0] + 1
    height = nonzero_pixels[3] - nonzero_pixels[1] + 1

    # 计算缩放因子
    resize_factor = 1
    if options["resize"]:
        max_length = max(width, height)
        min_length = min(width, height)
        if (max_length / min_length) > 1.25:
            resize_factor = (15 / 16) / (max_length / ori_image.size[0])
        else:
            resize_factor = (7 / 8) / (max_length / ori_image.size[0])

    print(resize_factor)
    desired_width = math.ceil(resize_factor * width)
    desired_height = math.ceil(resize_factor * height)
    crop_image = ori_image.crop(nonzero_pixels)
    resize_image = crop_image.resize((desired_width, desired_height))

    new_image = Image.new("RGBA", (image.shape[0], image.shape[1]))

    # 计算新图像的中心位置
    center_x = new_image.width // 2
    center_y = new_image.height // 2

    # 计算源图像粘贴的位置
    paste_x = center_x - (desired_width // 2)
    paste_y = center_y - (desired_height // 2)
    new_image.paste(resize_image, (paste_x, paste_y))

    return np.array(new_image)
