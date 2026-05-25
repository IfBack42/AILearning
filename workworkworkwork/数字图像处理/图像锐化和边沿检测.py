import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
==============================================
第 6 章：图像锐化与边缘检测
==============================================

这一章解决的问题：
    图像中哪些地方变化最明显？怎样把物体轮廓、文字边界、结构边缘提取出来？

边缘是什么：
    边缘通常出现在灰度值变化很剧烈的位置。
    比如黑色文字和白纸之间、物体和背景之间、亮暗区域交界处。

数学直觉：
    如果把灰度值看成高度，那么边缘就是高度变化很陡的地方。
    因此边缘检测经常和“导数”“梯度”有关。

常见方法：
    1. Sobel：
        一阶梯度算子，可以分别检测 x 方向和 y 方向变化。

    2. Scharr：
        Sobel 在 3x3 情况下的改进版本，方向响应更准确。

    3. Laplacian：
        二阶导数算子，不区分 x/y 方向，对噪声敏感，也常用于锐化。

    4. Canny：
        完整的边缘检测流程，包括去噪、梯度、非极大值抑制、双阈值连接。

锐化和边缘的关系：
    边缘代表图像细节；
    锐化就是增强这些细节，让图像看起来更清晰。

工程意义：
    1. 图像分割前用边缘帮助定位目标边界。
    2. 工业检测中提取零件轮廓。
    3. OCR 中增强文字边缘。
    4. 后续轮廓检测、形状分析的前置步骤。
==============================================
"""


def show_images(images, titles):
    """并排显示多张灰度图。"""
    plt.figure(figsize=(5 * len(images), 5))
    for i, (image, title) in enumerate(zip(images, titles), start=1):
        plt.subplot(1, len(images), i)
        plt.imshow(image, cmap="gray")
        plt.title(title)
        plt.axis("off")
    plt.tight_layout()
    plt.show()


def sobel_demo(image, ksize=3):
    """
    Sobel 边缘检测。

    image:
        输入灰度图。

    ksize:
        卷积核大小，常用 3、5、7，必须是正奇数。

    dx=1, dy=0:
        检测 x 方向灰度变化，容易突出竖直边缘。

    dx=0, dy=1:
        检测 y 方向灰度变化，容易突出水平边缘。

    注意：
        Sobel 结果可能有负数，所以先用 cv2.CV_64F 保存，
        再用 cv2.convertScaleAbs 转成可显示的 uint8。
    """
    grad_x = cv2.Sobel(image, cv2.CV_64F, dx=1, dy=0, ksize=ksize)
    grad_y = cv2.Sobel(image, cv2.CV_64F, dx=0, dy=1, ksize=ksize)

    abs_x = cv2.convertScaleAbs(grad_x)
    abs_y = cv2.convertScaleAbs(grad_y)

    # 把 x 和 y 两个方向的边缘融合到一张图中。
    edge = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    return abs_x, abs_y, edge


def laplacian_sharpen(image, strength=0.7):
    """
    Laplacian 锐化。

    原理：
        Laplacian 可以提取二阶边缘信息。
        原图减去一部分 Laplacian，可以增强图像细节。

    strength:
        锐化强度。越大越锐，但过大可能出现噪声和白边。
    """
    lap = cv2.Laplacian(image, cv2.CV_64F, ksize=3)
    edge = cv2.convertScaleAbs(lap)

    sharpened = image.astype(np.float64) - strength * lap
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
    return edge, sharpened


def canny_demo(image, threshold1=35, threshold2=160):
    """
    Canny 边缘检测。

    threshold1:
        低阈值。用于连接弱边缘。

    threshold2:
        高阈值。大于该值的边缘被认为是强边缘。

    简单理解：
        高阈值越大，保留下来的强边缘越少；
        低阈值越小，越容易连接弱边缘，但也可能引入噪声。
    """
    return cv2.Canny(image, threshold1, threshold2)


if __name__ == "__main__":
    img_path = "arknights.jpg"
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img_gray is None:
        print("图片路径错误，请检查 img_path")
        exit()

    print("shape:", img_gray.shape)
    print("dtype:", img_gray.dtype)
    print("min/max:", img_gray.min(), img_gray.max())

    # 简单演示：高斯滤波 + Canny。
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), sigmaX=0)
    canny_edge = canny_demo(img_blur, threshold1=35, threshold2=160)

    show_images(
        [img_gray, img_blur, canny_edge],
        ["Original", "Gaussian Blur", "Canny Edge"]
    )
