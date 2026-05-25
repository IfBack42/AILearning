import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
==============================================
第 3 章：图像平滑滤波
==============================================

这一章解决的问题：
    图像中有噪声时，怎样让图像变得更平滑、更干净？

什么是噪声：
    噪声可以理解为图像中不属于真实场景的随机干扰。
    比如低光照拍摄产生的颗粒感，或者图像中随机出现的黑白点。

平滑滤波的基本思想：
    一个像素不要只看自己，而是参考周围邻域像素。
    如果周围大多数像素都比较接近，那么孤立的异常点就可以被削弱。

常见方法：
    1. 均值滤波：
        用邻域平均值替代中心像素。
        简单、快，但容易模糊边缘。

    2. 中值滤波：
        用邻域中位数替代中心像素。
        对椒盐噪声非常有效，且相对保护边缘。

    3. 高斯滤波：
        距离中心越近的像素权重越大。
        比均值滤波自然，常作为边缘检测前的去噪步骤。

工程意义：
    1. Canny 边缘检测前通常先高斯滤波。
    2. 阈值分割前先去噪，可以减少二值图中的小噪点。
    3. 工业检测、医学图像、监控图像中都经常需要去噪。
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


def salt_pepper_noise(image, prob=0.02):
    """
    给图像添加椒盐噪声。

    prob:
        噪声比例。值越大，随机黑白点越多。

    椒盐噪声特点：
        一部分像素突然变成 0，另一部分像素突然变成 255。
    """
    output = image.copy()
    rand = np.random.rand(*image.shape)
    output[rand < prob / 2] = 0
    output[rand > 1 - prob / 2] = 255
    return output


def gaussian_noise(image, mean=0, sigma=25):
    """
    给图像添加高斯噪声。

    mean:
        噪声均值。

    sigma:
        噪声标准差。越大，噪声越明显。

    高斯噪声特点：
        像素值在原来的基础上随机上下波动。
    """
    image_float = image.astype(np.float32)
    noise = np.random.normal(mean, sigma, image.shape)
    noisy = image_float + noise
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    return noisy


def mean_filter(image, ksize=3):
    """
    均值滤波。

    原理：
        用 ksize x ksize 邻域内所有像素的平均值替代中心像素。

    优点：
        简单、速度快。

    缺点：
        容易把边缘也一起模糊掉。
    """
    return cv2.blur(image, (ksize, ksize))


def median_filter(image, ksize=3):
    """
    中值滤波。

    原理：
        对邻域像素排序，取中间值替代中心像素。

    优点：
        对椒盐噪声特别有效。

    注意：
        ksize 必须是大于 1 的奇数，比如 3、5、7。
    """
    return cv2.medianBlur(image, ksize)


def gaussian_filter(image, ksize=3, sigma=0):
    """
    高斯滤波。

    原理：
        使用高斯核做加权平均，越靠近中心的像素权重越大。

    适合：
        处理较自然的随机噪声，也常作为边缘检测前的预处理。
    """
    return cv2.GaussianBlur(image, (ksize, ksize), sigma)


if __name__ == "__main__":
    img_path = "./output/adaptive_threshold.jpg"
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img_gray is None:
        print("图片路径错误，请检查 img_path")
        exit()

    print("shape:", img_gray.shape)
    print("dtype:", img_gray.dtype)
    print("min/max:", img_gray.min(), img_gray.max())

    # 简单演示：椒盐噪声 + 中值滤波。
    # noisy = salt_pepper_noise(img_gray, prob=0.05)
    # denoised = median_filter(noisy, ksize=3)
    denoised = median_filter(img_gray, ksize=3)
    cv2.imwrite('./1.jpg',denoised)
    show_images(
        # [img_gray, noisy, denoised],
        [img_gray, denoised],
        # ["Original", "Salt-Pepper Noise", "Median Filter"]
        ["Original","Median Filter"]
    )
