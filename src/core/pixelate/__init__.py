import time

import numpy as np

from core.pixelate.transform import transform


def pixelate(image: np.ndarray, options: dict) -> np.ndarray:
    """图片像素画处理

    Args:
        image (np.ndarray): 图像矩阵
        options (dict): config.stylize_options

    Returns:
        np.ndarray: 像素画后的图像矩阵
    """
    resolution = options["resolution"]
    ratioX = image.shape[0] // resolution
    ratioY = image.shape[1] // resolution
    out_image = np.zeros((resolution, resolution, 4), dtype=np.uint8)
    for x in range(resolution):
        for y in range(resolution):
            image_block = image[
                x * ratioX : (x + 1) * ratioX, y * ratioY : (y + 1) * ratioY
            ]
            out_image[x, y] = transform(image_block, options)
    time2 = time.time()
    return out_image


__all__ = [pixelate]
