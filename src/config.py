config = {
    # 原始图像文件路径，支持相对路径与绝对路径
    "origin_dir": "./image/origin",
    # 导出图像文件路径，支持相对路径与绝对路径
    "out_dir": "./image/out",
    # 预处理参数
    "pretreat_options": {
        "resize": True,  # 是否缩放以保持边缘空白
    },
    # 像素化参数
    "pixelate_options": {
        "resolution": 16,  # 导出图像的像素
        "alpha_skip": 1,  # 不透明度低于此值的像素将不被计算
        "count_ratio": 0.3,  # 像素化比例，被计算的像素/总像素，大于此值才生成结果像素
        "hue_ratio": 0.3,  # 像素占比超过此值，将排除其他像素的影响
        "hue_range": 3,  # 像素色相区域范围
        "channel_depth": 8,  # 图像 rgba 通道位深度
    },
    # 风格化参数
    "stylize_options": {
        # 是否在风格化过程中调整图像 hsv，如果为 False，所有与 hsv 调整相关的操作都会被禁止
        "adjust": True,
        "analyze": True,  # 是否根据目标图像进行风格化
        "analyze_dir": "./image/analyze",  # 风格化图像文件路径，支持相对路径与绝对路径
        "adjust_h": False,  # 是否调整色相，和目标图像一致
        "adjust_s": True,  # 是否调整饱和度，和目标图像一致
        "adjust_v": True,  # 是否调整明度，和目标图像一致
        "factor_h": 0,  # 色相调整系数，加法运算
        "factor_s": 1,  # 饱和度调整系数，乘法运算
        "factor_v": 1.2,  # 明度调整系数，乘法运算
        "target_h": None,  # 调整图像的色相，覆盖目标图像分析结果
        "target_s": None,  # 调整图像的饱和度，覆盖目标图像分析结果
        "target_v": None,  # 调整图像的明度，覆盖目标图像分析结果
        # 是否使用滤镜，处理像素边缘
        "filter": True,
        "side": True,  # 是否将图片四周像素风格化
    },
}
