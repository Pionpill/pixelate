import numpy as np

from core.stylize.adjust import adjust
from core.stylize.filter import filter


def stylize(image: np.ndarray, options: dict) -> np.ndarray:
    """图像 MC 风格化

    Args:
        image (np.ndarray): 图像矩阵
        options (dict): config.stylize_options

    Returns:
        np.ndarray: 图像举证
    """
    adjust_image = adjust(image, options) if options["adjust"] else image
    filter_image = filter(adjust_image, options)
    return filter_image
