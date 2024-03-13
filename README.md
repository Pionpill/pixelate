# 像素化图片
分析已有图像的风格，将位图图片(.png, .jeg)转换为 MC 风格的像素画图片

<img src="./image/origin/example.png" width="100px"/>
<img src="./image/analyze/glow_berries.png" width="100px"/>
<img src="./image/out/example.png" width="100px"/>

## 项目启动
### 开发环境:

本人的开发环境，安装对应的模块即可运行:
- python: 3.11.4
- numpy: 1.25.2
- opencv-python: 4.8.0.76
- pillow: 10.0.0

安装对应 python 模块:

```bash
pip install numpy
pip install pillow
pip install opencv-python
```

### 启动步骤

图片像素化步骤
- 将原始图片放在 image/origin 目录下
  - 已经放了一张，支持批量处理，支持文件嵌套
- 将需要保持风格的图片放在 image/analyze 目录下
  - 已经放了一张，支持文件嵌套，多文件取平均值
- 运行 src 目录的脚本
- 将在 image/out 目录生成对应的图片

已经存放了一组图像，将 image/out 中的图像删除可以测试脚本

src/config.py 文件中可以进行一些参数配置

### 项目功能

为了和 MC 风格保持一致，脚本对图像做了如下调整(可以通过 config 调整对应功能):
- 删除不透明像素
- 使用硬边缘的方式进行缩放
- 尽量减少颜色过渡
- 图像自动居中，且保留边缘的 2/16 空白处
- 根据现有图像分析 hsv 并应用到目标图像上

项目仍处于开发过程中，如有任何 BUG 请联系本人