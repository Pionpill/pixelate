import logging
import os

import numpy as np
from PIL import Image, UnidentifiedImageError

from core.pixelate import pixelate
from core.pretreat import pretreat
from core.stylize import stylize


def process(file_path: str, config: dict) -> None:
    """MC 化处理，将图片保存在对应的 out 目录下

    Args:
        file_path (str): 文件绝对路径
        config (dict): config 对象
    """
    try:
        image = np.array(Image.open(file_path))
        image = pretreat(image, config["pretreat_options"])
        image = pixelate(image, config["pixelate_options"])
        image = stylize(image, config["stylize_options"])
        image = Image.fromarray(image)

        origin_dir = os.path.abspath(config["origin_dir"])
        out_dir = os.path.abspath(config["out_dir"])
        image.save(file_path.replace(origin_dir, out_dir))
    except UnidentifiedImageError as e:
        pass
    except Exception as e:
        print(f"全局错误: {file_path}: {logging.exception(e)}")


def batch_process(dir_path: str, config: dict):
    """目标文件夹下图像批处理

    Args:
        dir_path (str): 目标文件夹
        config (dict): config 对象
    """
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            batch_process(item_path, config)
        process(item_path, config)
