import itertools
import math

import cv2
import numpy as np


def get_pixel_hue(pixel: tuple[int]) -> float:
    Hue = math.atan2(
        np.sqrt(3) * (int(pixel[1]) - pixel[2]), 2 * pixel[0] - pixel[1] - pixel[2]
    )
    return (Hue / np.pi) * 180


def get_image_hsv(image: np.ndarray) -> tuple[float, float, float]:
    """获取图像整体 hsv 值: 跳过完全透明的像素，计算平均值

    Args:
        image (np.ndarray): 图像

    Returns:
        tuple[float, float, float]: (h, s, v) 分别代表色相，饱和度，亮度
    """
    rgba_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    alpha_channel = rgba_image[:, :, 3]

    total_hue = 0
    total_saturation = 0
    total_value = 0
    pixel_count = 0

    for i in range(rgba_image.shape[0]):
        for j in range(rgba_image.shape[1]):
            if alpha_channel[i, j] == 0:
                continue
            pixel = rgba_image[i, j]
            hsv_pixel = cv2.cvtColor(np.array([[pixel]]), cv2.COLOR_RGB2HSV)[0][0]
            hue, saturation, value = hsv_pixel[0], hsv_pixel[1], hsv_pixel[2]

            total_hue += hue
            total_saturation += saturation
            total_value += value
            pixel_count += 1

    avg_hue = total_hue / pixel_count
    avg_saturation = total_saturation / pixel_count
    avg_value = total_value / pixel_count
    return avg_hue, avg_saturation, avg_value


def adjust_image_hsv(
    image: np.ndarray, target_hsv: tuple[float, float, float], hsv_include: tuple
) -> np.ndarray:
    """调整图像的 hsv

    Args:
        image (np.ndarray): 要调整的图像矩阵
        target_hsv (tuple[float, float, float]): 调整的目标 hsv 元组
        adjust_hsv (tuple): 要调整的对象，包含 'h' / 's' / 'v'，表示对应参数需要调整

    Returns:
        np.ndarray: 调整后的图像矩阵
    """
    if "h" not in hsv_include and "v" not in hsv_include and "s" not in hsv_include:
        return image

    image_hsv = get_image_hsv(image)
    (s_scale, v_scale) = tuple(
        target_hsv[i] / image_hsv[i] for i in range(1, len(image_hsv))
    )
    h_shift = target_hsv[0] - image_hsv[0] if "h" in hsv_include else None

    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    alpha_channel = image[:, :, 3]

    # hsv 调整
    for i in range(hsv_image.shape[0]):
        for j in range(hsv_image.shape[1]):
            if alpha_channel[i, j] == 0:
                continue
            if "h" in hsv_include:
                hsv_image[i, j, 0] = abs(hsv_image[i, j, 0] + h_shift) % 360
            if "s" in hsv_include:
                hsv_image[i, j, 1] = np.clip(hsv_image[i, j, 1] * s_scale, 0, 255)
            if "v" in hsv_include:
                hsv_image[i, j, 2] = np.clip(hsv_image[i, j, 2] * v_scale, 0, 255)

    rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)

    # 重置 alpha 通道
    out_image = image.copy()
    for i, j in itertools.product(range(image.shape[0]), range(image.shape[1])):
        out_image[i, j] = np.append(rgb_image[i, j], image[i, j][3])
    return np.array(out_image)
