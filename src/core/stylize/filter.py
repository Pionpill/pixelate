import itertools

import cv2
import numpy as np


def __is_edge_pixel(
    alpha_channel: np.ndarray, position: tuple[int, int], side: bool
) -> bool:
    (x, y) = position

    if alpha_channel[x, y] == 0:
        return False
    if x == 0 or y == 0:
        return side
    (width, height) = alpha_channel.shape
    if x >= (width - 1) or y >= (height - 1):
        return side

    if (
        alpha_channel[x - 1, y] == 0
        or alpha_channel[x + 1, y] == 0
        or alpha_channel[x, y - 1] == 0
        or alpha_channel[x, y + 1] == 0
    ):
        return True


def filter(image: np.ndarray, options: dict) -> np.ndarray:
    alpha_channel = image[:, :, 3]
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    if not options["filter"]:
        return image
    for i, j in itertools.product(range(hsv_image.shape[0]), range(hsv_image.shape[1])):
        if __is_edge_pixel(alpha_channel, (i, j), options["side"]):
            hsv_image[i, j, 2] = np.clip(hsv_image[i, j, 2] - 35, 0, 255)

    rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
    out_image = image.copy()
    for i, j in itertools.product(range(image.shape[0]), range(image.shape[1])):
        out_image[i, j] = np.append(rgb_image[i, j], image[i, j][3])
    return out_image
