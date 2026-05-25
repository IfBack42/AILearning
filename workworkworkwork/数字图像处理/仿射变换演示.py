import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
==============================================
第 5 章：图像几何变换：仿射变换
==============================================

这一章解决的问题：
    图像中的物体位置、角度、大小发生变化时，怎样通过数学变换把它移动、旋转或缩放？

仿射变换可以完成：
    1. 平移
    2. 缩放
    3. 旋转
    4. 剪切
    5. 镜像
    6. 上面几种变换的组合

仿射变换的特点：
    直线变换后仍然是直线；
    平行线变换后仍然平行。

OpenCV 中的仿射矩阵是 2x3：

    [ a  b  tx ]
    [ c  d  ty ]

对像素点 (x, y)，变换公式是：

    x' = a*x + b*y + tx
    y' = c*x + d*y + ty

其中：
    a, b, c, d 控制旋转、缩放、剪切、镜像；
    tx, ty 控制平移。

常用 API：
    cv2.warpAffine(src, M, dsize)

工程意义：
    1. OCR 中矫正文档角度。
    2. 数据增强中随机旋转、平移、缩放图像。
    3. 目标检测/分割训练时，图像和标签 mask 必须做一致的几何变换。
==============================================
"""


def show_images(images, titles):
    """并排显示多张 RGB 图像。"""
    plt.figure(figsize=(5 * len(images), 5))
    for i, (image, title) in enumerate(zip(images, titles), start=1):
        plt.subplot(1, len(images), i)
        plt.imshow(image)
        plt.title(title)
        plt.axis("off")
    plt.tight_layout()
    plt.show()


def transform_points(points, M):
    """
    手动计算点坐标的仿射变换。

    points:
        原始点坐标，形状为 (N, 2)，每一行是 [x, y]。

    M:
        2x3 仿射矩阵。

    这个函数的目的不是替代 OpenCV，而是帮助你理解矩阵公式。
    """
    new_points = []
    for x, y in points:
        new_x = M[0, 0] * x + M[0, 1] * y + M[0, 2]
        new_y = M[1, 0] * x + M[1, 1] * y + M[1, 2]
        new_points.append([new_x, new_y])
    return np.array(new_points)


def apply_affine(image, M):
    """
    对整张图像执行仿射变换。

    image:
        RGB 图像。

    M:
        2x3 仿射矩阵。

    dsize:
        OpenCV 中输出尺寸顺序是 (width, height)，不是 (height, width)。
    """
    rows, cols = image.shape[:2]
    M = np.float32(M)
    return cv2.warpAffine(image, M, dsize=(cols, rows))


def get_translate_matrix(tx, ty):
    """
    平移矩阵。

    tx > 0 图像向右移动；
    ty > 0 图像向下移动。
    """
    return np.float32([
        [1, 0, tx],
        [0, 1, ty]
    ])


def get_rotate_matrix(image, angle, scale=1.0):
    """
    旋转矩阵。

    angle:
        旋转角度。正数表示逆时针旋转。

    scale:
        缩放比例。1.0 表示保持原大小。
    """
    rows, cols = image.shape[:2]
    center = (cols / 2, rows / 2)
    return cv2.getRotationMatrix2D(center, angle, scale)


def get_reflect_x_matrix(image):
    """
    左右镜像矩阵。

    x' = -x + cols - 1
    y' = y
    """
    rows, cols = image.shape[:2]
    return np.float32([
        [-1, 0, cols - 1],
        [0, 1, 0]
    ])


if __name__ == "__main__":
    image_path = "naixu.jpg"
    img_bgr = cv2.imread(image_path)

    if img_bgr is None:
        print("图片路径错误，请检查 image_path")
        exit()

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    print("shape:", img_rgb.shape)
    print("dtype:", img_rgb.dtype)

    # 简单演示：旋转。
    M_rotate = get_rotate_matrix(img_rgb, angle=30, scale=1.0)
    img_rotate = apply_affine(img_rgb, M_rotate)

    show_images(
        [img_rgb, img_rotate],
        ["Original", "Rotate 30 Degrees"]
    )
