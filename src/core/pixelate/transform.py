import itertools
import time

import numpy as np

from utils.hsv import get_pixel_hue


def __get_matrix_hueMap(matrix: np.ndarray, options: dict) -> tuple:
    """获取像素矩阵的色相信息，返回两个数据，计算的像素总量，色相字典

    Args:
        matrix (np.ndarray): 像素举证
        options (dict): config.pixelate_options

    Returns:
        tuple: (pixel_count, { "count": number, "sum_red": number, "sum_green": number, "sum_blue": number, "sum_alpha": number})
    """
    pixel_count = 0
    hue_map = {}
    for x, y in itertools.product(range(len(matrix)), range(len(matrix[0]))):
        pixel = matrix[x, y]
        if pixel[3] < 255 * options["alpha_skip"]:
            continue
        pixel_count += 1
        pixel_hue_key = round(get_pixel_hue(pixel) // options["hue_range"])
        if pixel_hue_key in hue_map:
            hue_value = hue_map[pixel_hue_key]
            hue_value["count"] += 1
            hue_value["sum_red"] += pixel[0]
            hue_value["sum_green"] += pixel[1]
            hue_value["sum_blue"] += pixel[2]
            hue_value["sum_alpha"] += pixel[3]
        else:
            hue_map[pixel_hue_key] = {
                "count": 1,
                "sum_red": int(pixel[0]),
                "sum_green": int(pixel[1]),
                "sum_blue": int(pixel[2]),
                "sum_alpha": int(pixel[3]),
            }
    return (pixel_count, hue_map)


def transform(matrix: np.ndarray, options: dict) -> list[int]:
    """将指定范围内的图像矩阵取均值转化为单个像素

    Args:
        arr (np.ndarray): 图像矩阵
        options (dict): config.pixelate_options

    Returns:
        list[int]: 单个像素元素
    """
    (pixel_count, hue_map) = __get_matrix_hueMap(matrix, options)

    count = 0
    sum_red = 0
    sum_green = 0
    sum_blue = 0
    sum_alpha = 0

    target_value = {"count": 0}

    for value in hue_map.values():
        count += value["count"]
        sum_red += value["sum_red"]
        sum_green += value["sum_green"]
        sum_blue += value["sum_blue"]
        sum_alpha += value["sum_alpha"]
        if value["count"] > target_value["count"]:
            target_value = value

    if target_value["count"] > options["hue_ratio"] * pixel_count:
        count = target_value["count"]
        sum_red = target_value["sum_red"]
        sum_green = target_value["sum_green"]
        sum_blue = target_value["sum_blue"]
        sum_alpha = target_value["sum_alpha"]

    matrix_pixel_count = matrix.shape[0] * matrix.shape[1]
    if pixel_count == 0 or pixel_count < options["count_ratio"] * matrix_pixel_count:
        return [0, 0, 0, 0]
    channel_factor = 2 ** (8 - options["channel_depth"])
    return [
        sum_red // (count * channel_factor) * channel_factor,
        sum_green // (count * channel_factor) * channel_factor,
        sum_blue // (count * channel_factor) * channel_factor,
        sum_alpha // count,
    ]
