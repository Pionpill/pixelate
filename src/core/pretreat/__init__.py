import numpy as np

from core.pretreat.resize import resize


def pretreat(image: np.ndarray, options: dict) -> np.ndarray:
    return resize(image, options)
