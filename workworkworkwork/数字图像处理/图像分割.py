import os

import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
==============================================
第 7 章：图像分割：阈值分割
==============================================

这一章解决的问题：
    怎样把图像中的目标区域和背景区域分开？

边缘检测和图像分割的区别：
    边缘检测关注“边界在哪里”；
    图像分割关注“哪些像素属于目标”。

阈值分割：
    这是最基础、最直观的一类图像分割方法。
    它根据像素灰度值是否超过某个阈值，把像素分成两类。

灰度图像素范围通常是 [0, 255]：
    0   表示黑
    255 表示白

二值分割结果通常只有两个值：
    0   表示背景
    255 表示目标

公式：
    g(x, y) = 255,  if f(x, y) >= T
    g(x, y) = 0,    if f(x, y) <  T

手动阈值：
    阈值 T 由我们自己指定。
    优点是简单直观；
    缺点是阈值不好选，换一张图可能就不合适。

其中：
    f(x, y) 是原图灰度值；
    T 是手动设置的阈值；
    g(x, y) 是分割后的二值图。

Otsu 大津阈值：
    Otsu 会自动帮我们寻找一个全局阈值。

    它的核心思想是：
        遍历所有可能的灰度阈值；
        每个阈值都把图像分成前景和背景两类；
        选择让两类内部最稳定、两类之间差异最大的那个阈值。

    换句话说：
        类内方差尽量小；
        类间方差尽量大。

    Otsu 适合：
        前景和背景灰度差异明显；
        光照比较均匀；
        灰度直方图大致有两个峰。

自适应阈值：
    手动阈值和 Otsu 都属于全局阈值，也就是整张图共用一个 T。
    自适应阈值不是这样。

    它的核心思想是：
        每个像素都根据自己附近的一小块区域，计算一个局部阈值。

    所以它更适合：
        光照不均匀；
        有阴影；
        文档扫描、文字提取等场景。

    常见局部阈值计算方式：
        1. 邻域平均值 - C
        2. 邻域高斯加权平均值 - C

适合场景：
    1. 目标和背景灰度差异明显。
    2. 光照比较均匀。
    3. 白纸黑字、黑背景白物体、简单工业零件等。

局限性：
    1. 手动阈值需要人工选择。
    2. Otsu 对光照不均匀的图像容易失败。
    3. 自适应阈值虽然能处理局部光照变化，但参数 block_size 和 C 需要调。
    4. 背景复杂时，传统阈值方法仍然可能不够。

和深度学习分割的关系：
    手动阈值是人工写规则得到 mask；
    SegNet、U-Net 这类模型是通过训练数据学习如何预测 mask。
    它们的结果都可以看成“每个像素属于哪里”。
==============================================
"""


def show_images(images, titles):
    """并排显示多张灰度图。"""
    plt.figure(figsize=(5 * len(images), 6))
    for i, (image, title) in enumerate(zip(images, titles), start=1):
        plt.subplot(1, len(images), i)
        plt.imshow(image, cmap="gray")
        plt.title(title)
        plt.axis("off")
    plt.tight_layout()
    plt.show()


def manual_threshold(image, threshold=127, max_value=255, mode="binary"):
    """
    手动阈值分割。

    image:
        输入灰度图。

    threshold:
        阈值。像素值与它比较，决定属于前景还是背景。

    max_value:
        前景像素值，通常是 255。

    mode:
        "binary":
            像素值 >= threshold 变成 max_value；
            像素值 < threshold 变成 0。

        "binary_inv":
            像素值 >= threshold 变成 0；
            像素值 < threshold 变成 max_value。
            适合目标比背景暗的情况，比如白纸黑字。

    返回：
        二值图。
    """
    if mode == "binary":
        result = np.where(image >= threshold, max_value, 0)
    elif mode == "binary_inv":
        result = np.where(image >= threshold, 0, max_value)
    else:
        raise ValueError("mode 只能是 'binary' 或 'binary_inv'")

    return result.astype(np.uint8)


def otsu_threshold(image, max_value=255, mode="binary"):
    """
    Otsu 大津阈值分割。

    image:
        输入灰度图。

    max_value:
        前景像素值，通常是 255。

    mode:
        "binary":
            目标比背景亮时常用。

        "binary_inv":
            目标比背景暗时常用，比如白纸黑字。

    原理简述：
        Otsu 不需要我们手动指定 threshold。
        它会自动遍历 0-255 之间的阈值，寻找一个最优阈值。

    返回：
        best_threshold:
            Otsu 自动找到的阈值。

        binary:
            根据 best_threshold 得到的二值图。
    """
    if mode == "binary":
        threshold_type = cv2.THRESH_BINARY + cv2.THRESH_OTSU
    elif mode == "binary_inv":
        threshold_type = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    else:
        raise ValueError("mode 只能是 'binary' 或 'binary_inv'")

    best_threshold, binary = cv2.threshold(
        image,
        0,
        max_value,
        threshold_type
    )

    return best_threshold, binary


def adaptive_threshold(
    image,
    max_value=255,
    method="gaussian",
    mode="binary",
    block_size=11,
    c=2
):
    """
    自适应阈值分割。

    image:
        输入灰度图。

    max_value:
        前景像素值，通常是 255。

    method:
        "mean":
            局部均值法，阈值 = 邻域平均灰度 - c。

        "gaussian":
            局部高斯加权法，距离中心越近的像素权重越大。

    mode:
        "binary":
            当前像素大于局部阈值时变成 max_value。

        "binary_inv":
            当前像素大于局部阈值时变成 0。

    block_size:
        局部窗口大小，必须是大于 1 的奇数，例如 11、15、21。
        窗口越小，对局部变化越敏感；
        窗口越大，结果越稳定，但细节可能变少。

    c:
        从局部均值或高斯加权均值中减去的常数。
        在 THRESH_BINARY 模式下，c 越大，局部阈值越低，白色区域通常越多。

    返回：
        二值图。
    """
    if block_size <= 1 or block_size % 2 == 0:
        raise ValueError("block_size 必须是大于 1 的奇数")

    if method == "mean":
        adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
    elif method == "gaussian":
        adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    else:
        raise ValueError("method 只能是 'mean' 或 'gaussian'")

    if mode == "binary":
        threshold_type = cv2.THRESH_BINARY
    elif mode == "binary_inv":
        threshold_type = cv2.THRESH_BINARY_INV
    else:
        raise ValueError("mode 只能是 'binary' 或 'binary_inv'")

    return cv2.adaptiveThreshold(
        image,
        max_value,
        adaptive_method,
        threshold_type,
        block_size,
        c
    )


if __name__ == "__main__":
    img_path = "arknights.jpg"
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img_gray is None:
        print("图片路径错误，请检查 img_path")
        exit()

    print("shape:", img_gray.shape)
    print("dtype:", img_gray.dtype)
    print("min/max:", img_gray.min(), img_gray.max())

    # 演示 1：手动阈值。
    threshold = 150
    manual_binary = manual_threshold(img_gray, threshold=threshold, mode="binary")

    show_images(
        [img_gray, manual_binary],
        ["Original Gray", f"Manual Threshold T={threshold}"]
    )

    # 演示 2：Otsu 自动阈值。
    otsu_value, otsu_binary = otsu_threshold(img_gray, mode="binary")
    print("Otsu 自动找到的阈值:", otsu_value)

    show_images(
        [img_gray, otsu_binary],
        ["Original Gray", f"Otsu Threshold T={otsu_value:.0f}"]
    )

    # 演示 3：自适应阈值。
    adaptive_binary = adaptive_threshold(
        img_gray,
        method="gaussian",
        mode="binary",
        block_size=11,
        c=12
    )

    show_images(
        [img_gray, adaptive_binary],
        ["Original Gray", "Adaptive Threshold"]
    )

    os.makedirs("./output", exist_ok=True)
    cv2.imwrite("./output/manual_threshold.jpg", manual_binary)
    cv2.imwrite("./output/otsu_threshold.jpg", otsu_binary)
    cv2.imwrite("./output/adaptive_threshold.jpg", adaptive_binary)
