import logging
import os

import numpy as np
from PIL import Image, UnidentifiedImageError

from utils import hsv


def __batch_analyze(
    dir_path: str, sum_hsv: list[float] = None, count=0
) -> list[int, list[float]]:
    """分析文件夹下所有图像文件的 hsv 值，返回总计

    Args:
        dir_path (str): 文件夹路径
        sum_hsv (tuple[float]): 目前获取的 [h, s, v] 总和列表. 默认为 None
        count (int, optional): 目前分析的图像总数. Defaults to 0.

    Returns:
        tuple[int, tuple[float]: [总数, [sum_h, sum_s, sum_v]]
    """
    if sum_hsv is None:
        sum_hsv = [0, 0, 0]
    for item in os.listdir(os.path.abspath(dir_path)):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            [count, _] = __batch_analyze(item_path)
        try:
            image = np.array(Image.open(item_path))
            item_hsv = hsv.get_image_hsv(image)
            sum_hsv = [sum_hsv[i] + item_hsv[i] for i in range(len(item_hsv))]
            count += 1
        except UnidentifiedImageError as e:
            pass
        except Exception as e:
            print(f"分析风格-文件格式不支持: {item_path}: {logging.exception(e)}")
    return [count, sum_hsv]


def analyze(filePath: str) -> tuple[float]:
    """分析目标文件下图像 hsv 值，取均值

    Args:
        filePath (str): 文件夹地址

    Returns:
        tuple[float]: [h, s ,v]
    """
    [count, sum_hsv] = __batch_analyze(filePath)
    return tuple(sum_hsv[i] / count for i in range(len(sum_hsv)))
