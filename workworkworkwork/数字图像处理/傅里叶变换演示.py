import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
==============================================
第 4 章：傅里叶变换与频域滤波
==============================================

这一章解决的问题：
    除了直接看像素，我们还能不能从“频率”的角度理解图像？

空间域：
    直接处理像素位置 (x, y) 上的灰度值。
    例如：滤波、锐化、边缘检测。

频域：
    把图像拆成很多不同频率的成分。
    低频通常对应图像的整体亮度和大轮廓；
    高频通常对应边缘、纹理、细节和噪声。

傅里叶变换的直观理解：
    一张图像可以看成很多“明暗波纹”的叠加。
    傅里叶变换就是把图像从“像素视角”转换到“频率视角”。

常见结论：
    1. 低频在频谱中心，代表整体结构。
    2. 高频在频谱外围，代表边缘和细节。
    3. 低通滤波会让图像变模糊。
    4. 高通滤波会突出边缘、纹理，也可能突出噪声。

工程意义：
    1. 理解 JPEG 压缩、DCT、频率成分。
    2. 去除周期性噪声。
    3. 从频域角度理解模糊、锐化和边缘。
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


def fft_spectrum(image):
    """
    计算图像的频谱图。

    步骤：
        1. np.fft.fft2 做二维傅里叶变换。
        2. np.fft.fftshift 把低频移动到图像中心。
        3. abs 取幅度。
        4. log 压缩显示范围，否则频谱中心会太亮。
    """
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    spectrum = np.log(1 + np.abs(fshift))
    return fshift, spectrum


def make_lowpass_mask(shape, radius):
    """
    创建理想低通滤波掩膜。

    mask 中心圆区域为 1，表示保留低频；
    其他区域为 0，表示去掉高频。
    """
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2

    mask = np.zeros((rows, cols), np.uint8)
    cv2.circle(mask, (ccol, crow), radius, 1, -1)
    return mask


def lowpass_filter(image, radius=30):
    """
    低通滤波。

    效果：
        保留低频，去掉高频。
        图像会变模糊，但整体轮廓还在。
    """
    fshift, _ = fft_spectrum(image)
    mask = make_lowpass_mask(image.shape, radius)

    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)
    filtered = np.abs(np.fft.ifft2(f_ishift))

    filtered = cv2.normalize(filtered, None, 0, 255, cv2.NORM_MINMAX)
    filtered = filtered.astype(np.uint8)
    return mask, filtered


def highpass_filter(image, radius=30):
    """
    高通滤波。

    效果：
        去掉中心低频，保留外围高频。
        结果通常表现为边缘、纹理和噪声。
    """
    fshift, _ = fft_spectrum(image)
    low_mask = make_lowpass_mask(image.shape, radius)
    high_mask = 1 - low_mask

    fshift_filtered = fshift * high_mask
    f_ishift = np.fft.ifftshift(fshift_filtered)
    filtered = np.abs(np.fft.ifft2(f_ishift))

    filtered = cv2.normalize(filtered, None, 0, 255, cv2.NORM_MINMAX)
    filtered = filtered.astype(np.uint8)
    return high_mask, filtered


if __name__ == "__main__":
    img_path = "naixu.jpg"
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img_gray is None:
        print("图片路径错误，请检查 img_path")
        exit()

    print("shape:", img_gray.shape)
    print("dtype:", img_gray.dtype)
    print("min/max:", img_gray.min(), img_gray.max())

    # 简单演示：查看频谱 + 低通滤波。
    _, spectrum = fft_spectrum(img_gray)
    low_mask, low_result = lowpass_filter(img_gray, radius=30)

    show_images(
        [img_gray, spectrum, low_mask * 255, low_result],
        ["Original", "FFT Spectrum", "Lowpass Mask", "Lowpass Result"]
    )
