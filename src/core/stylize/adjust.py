import numpy as np

from core.stylize.analyze import analyze
from utils import hsv


def __get_hsv_factor(options: dict) -> tuple[float]:
    """计算 hsv 调整因子

    Args:
        options (dict): config.stylize_options

    Returns:
        tuple[float]: [h, s, v]
    """
    factor_hsv = (options["factor_h"], options["factor_s"], options["factor_v"])
    if options["analyze"]:
        target_hsv = analyze(options["analyze_dir"])
        factor_hsv = (
            factor_hsv[0] + target_hsv[0],
            factor_hsv[1] * target_hsv[1],
            factor_hsv[2] * target_hsv[2],
        )
    return (
        options["target_h"] or factor_hsv[0],
        options["target_s"] or factor_hsv[1],
        options["target_v"] or factor_hsv[2],
    )


def __adjust_image(
    image: np.ndarray, options: dict, hsv_factor: tuple[float]
) -> np.ndarray:
    """根据参考图像调整颜色

    Args:
        image (np.ndarray): 源图像
        options (dict): config.analyze_options
        hsv_factor (dict): (h, s, v)

    Returns:
        np.ndarray: 结果图像
    """
    hsv_include = []
    if options["adjust_h"]:
        hsv_include.append("h")
    if options["adjust_s"]:
        hsv_include.append("s")
    if options["adjust_v"]:
        hsv_include.append("v")
    return hsv.adjust_image_hsv(image, hsv_factor, tuple(hsv_include))


def adjust(image: np.ndarray, options: dict) -> np.ndarray:
    """调整图像的整体风格

    Args:
        image (np.ndarray): 图像矩阵
        options (dict): config.stylize_options

    Returns:
        np.ndarray: 图像矩阵
    """
    if not options["adjust"]:
        return image
    hsv_factor = __get_hsv_factor(options)
    return __adjust_image(image, options, hsv_factor)
