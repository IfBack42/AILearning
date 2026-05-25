import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
==============================================
第 2 章：灰度变换与直方图均衡化
==============================================

这一章解决的问题：
    一张图太暗、太亮、对比度太低时，怎样通过改变像素灰度值，让图像更容易观察和处理？

核心思想：
    灰度图可以看成一个二维矩阵，每个像素值通常在 [0, 255] 之间。
    灰度变换就是把原来的像素值 r 映射成新的像素值 s：

        s = T(r)

    这里的 T 就是某种变换规则。

常见方法：
    1. 线性拉伸：
        把原图较窄的灰度范围拉开，提高对比度。

    2. 灰度反转：
        s = 255 - r
        黑变白，白变黑，常用于观察负片效果或增强暗目标。

    3. 直方图均衡化：
        根据整张图的灰度分布自动重新分配灰度值，让对比度更明显。

工程意义：
    1. 作为目标检测、分割、OCR 的预处理。
    2. 增强低对比度图像中的细节。
    3. 帮助我们观察图像灰度分布，为后续阈值分割选阈值。
==============================================
"""


def show_images(original, processed, title1="Original", title2="Processed"):
    """并排显示原图和处理结果，方便直接观察变化。"""
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap="gray")
    plt.title(title1)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(processed, cmap="gray")
    plt.title(title2)
    plt.axis("off")

    plt.tight_layout()
    plt.show()


def linear_stretch(image, a, b, c=0, d=255):
    """
    灰度线性拉伸。

    image:
        输入灰度图。

    a, b:
        原图中需要被拉伸的灰度范围。
        例如 a=40, b=200 表示把 [40, 200] 这段灰度重点拉开。

    c, d:
        输出灰度范围，通常设为 [0, 255]。

    公式：
        s = c + (d - c) / (b - a) * (r - a)

    注意：
        计算时先转成 float，避免 uint8 溢出；
        最后再裁剪到 [0, 255] 并转回 uint8。
    """
    image_float = image.astype(np.float32)
    stretched = c + (d - c) / (b - a) * (image_float - a)
    stretched = np.clip(stretched, 0, 255).astype(np.uint8)
    return stretched


def gray_invert(image):
    """
    灰度反转。

    原理：
        新像素值 = 255 - 原像素值

    效果：
        亮区域变暗，暗区域变亮。
    """
    return 255 - image


def histogram_equalize(image):
    """
    直方图均衡化。

    作用：
        自动增强整张图的对比度。

    适合：
        图像整体偏暗、偏亮，或者灰度集中在很窄范围内的情况。

    不适合：
        噪声很多的图像，因为它可能把噪声也增强。
    """
    return cv2.equalizeHist(image)


def plot_histogram(image, title="Histogram"):
    """
    绘制灰度直方图。

    横轴：
        灰度值 0-255。

    纵轴：
        每个灰度值出现的像素数量。

    直方图可以帮助判断：
        1. 图像整体偏暗还是偏亮。
        2. 对比度是否足够。
        3. 阈值分割时阈值大概可以取在哪里。
    """
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    plt.figure(figsize=(8, 4))
    plt.plot(hist, color="black")
    plt.xlim([0, 256])
    plt.xlabel("Pixel Value")
    plt.ylabel("Count")
    plt.title(title)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    img_path = "save.jpg"
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img_gray is None:
        print("图片路径错误，请检查 img_path")
        exit()

    print("shape:", img_gray.shape)
    print("dtype:", img_gray.dtype)
    print("min/max:", img_gray.min(), img_gray.max())

    # 简单演示：直方图均衡化。
    equalized = histogram_equalize(img_gray)
    show_images(img_gray, equalized, "Original", "Histogram Equalization")

    # 再看一下均衡化前后的直方图变化。
    plot_histogram(img_gray, "Original Histogram")
    plot_histogram(equalized, "Equalized Histogram")
