import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
==============================================
Sobel 算子
==============================================
作用：检测图像边缘，本质是计算灰度变化，属于一阶微分边缘检测。

Gx：检测 x 方向变化，常用于找竖直边缘
[-1, 0, 1]
[-2, 0, 2]
[-1, 0, 1]

Gy：检测 y 方向变化，常用于找水平边缘
[-1, -2, -1]
[ 0,  0,  0]
[ 1,  2,  1]

综合边缘：
G = sqrt(Gx^2 + Gy^2)
也可以近似使用：G = |Gx| + |Gy|

适用场景：
1. 提取物体轮廓、文字边缘、零件边界。
2. 作为轮廓检测、目标定位等任务的预处理。
3. 图像噪声较多时，建议先高斯滤波再 Sobel。

==============================================
Scharr 算子
==============================================

Scharr 可以理解为 Sobel 在 3x3 情况下的改进版，方向响应更准确。
当你想使用 3x3 边缘检测，并且希望边缘更明显时，可以优先试 Scharr。

Scharr Gx：
[ -3, 0,  3]
[-10, 0, 10]
[ -3, 0,  3]

Scharr Gy：
[ -3, -10, -3]
[  0,   0,  0]
[  3,  10,  3]

==============================================
Laplacian 算子
==============================================

Laplacian 是二阶微分算子，直接检测灰度突变位置，不区分 x / y 方向。
常用 3x3 核：
[ 0,  1,  0]
[ 1, -4,  1]
[ 0,  1,  0]

适用场景：
1. 快速提取整体边缘。
2. 图像锐化：原图减去二阶边缘信息，可以增强细节。
3. 对噪声敏感，通常先高斯滤波再做 Laplacian。

==============================================
Canny 边缘检测
==============================================

Canny 是更完整的边缘检测流程，不只是一个卷积核。
基本步骤：
1. 高斯滤波去噪
2. 计算梯度方向和强度
3. 非极大值抑制，让边缘变细
4. 双阈值筛选，连接强边缘和弱边缘

适用场景：
1. 想得到细、连续、干净的边缘。
2. 后续要做轮廓检测、形状分析、目标分割。
3. 比 Sobel / Scharr / Laplacian 更适合直接拿来做工程中的边缘图。

几种边缘检测的快速区别：
Sobel：一阶梯度，可分别看 x / y 方向边缘，简单直观。
Scharr：Sobel 的 3x3 改进版，边缘响应更强，方向更准确。
Laplacian：二阶算子，不区分方向，常用于锐化，但对噪声敏感。
Canny：完整边缘检测算法，边缘更细更稳定，参数稍多。
"""


def show_images(images, titles):
    """并排显示多张灰度图。"""
    plt.figure(figsize=(4 * len(images), 5))
    for i, (image, title) in enumerate(zip(images, titles), start=1):
        plt.subplot(1, len(images), i)
        plt.imshow(image, cmap='gray')
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()
    plt.show()


def sobel_demo(image, ksize=3):
    """
    image: 灰度图，通常是 uint8，像素范围 [0,255]
    ksize: Sobel 卷积核大小，常用 3、5、7，必须是正奇数

    cv2.Sobel(src, ddepth, dx, dy, ksize)
    src: 输入图像
    ddepth: 输出数据类型。这里用 cv2.CV_64F，防止负梯度被 uint8 截断
    dx: x 方向导数阶数，dx=1 表示求 x 方向梯度
    dy: y 方向导数阶数，dy=1 表示求 y 方向梯度
    ksize: 卷积核大小
    """
    # x 方向梯度：容易突出竖直边缘
    grad_x = cv2.Sobel(image, cv2.CV_64F, dx=1, dy=0, ksize=ksize)

    # y 方向梯度：容易突出水平边缘
    grad_y = cv2.Sobel(image, cv2.CV_64F, dx=0, dy=1, ksize=ksize)

    # Sobel 结果可能有负数，显示前要取绝对值并转回 uint8
    abs_x = cv2.convertScaleAbs(grad_x)
    abs_y = cv2.convertScaleAbs(grad_y)

    # API 融合 / 近似融合：
    # cv2.addWeighted 本质是做加权相加：
    # edge_add = abs_x * 0.5 + abs_y * 0.5 + 0
    #
    # 它不是 Sobel 的严格数学梯度幅值公式，而是把 x 和 y 两个方向的边缘图
    # 按比例叠加到一起。优点是简单、直观、速度快，复习和演示时很常用。
    #
    # 如果把权重改成 1 和 1，就接近常见近似形式：
    # G ≈ |Gx| + |Gy|
    edge_add = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)

    # 公式融合 / 梯度幅值融合：
    # 按照更标准的梯度幅值公式计算：
    # G = sqrt(Gx^2 + Gy^2)
    #
    # 这里使用的是 grad_x、grad_y 的原始浮点结果，而不是 abs_x、abs_y。
    # 原因是 grad_x、grad_y 保留了完整梯度数值，适合参与平方和开方计算。
    #
    # 计算完成后结果仍然是 float 类型，需要 normalize 到 [0,255]，
    # 再 astype(np.uint8)，才能作为普通灰度图显示。
    edge_magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
    edge_magnitude = cv2.normalize(edge_magnitude, None, 0, 255, cv2.NORM_MINMAX)
    edge_magnitude = edge_magnitude.astype(np.uint8)

    return abs_x, abs_y, edge_add, edge_magnitude


def scharr_demo(image):
    """
    Scharr 算子演示。

    cv2.Scharr(src, ddepth, dx, dy)
    src: 输入灰度图
    ddepth: 输出数据类型。仍然用 cv2.CV_64F，防止负梯度丢失
    dx: x 方向导数阶数
    dy: y 方向导数阶数

    注意：
    Scharr 不需要传 ksize，因为它固定使用改进的 3x3 卷积核。
    """
    # x 方向梯度：突出竖直边缘
    grad_x = cv2.Scharr(image, cv2.CV_64F, dx=1, dy=0)

    # y 方向梯度：突出水平边缘
    grad_y = cv2.Scharr(image, cv2.CV_64F, dx=0, dy=1)

    # 和 Sobel 一样，Scharr 原始结果可能有负数，显示前需要转成 uint8
    abs_x = cv2.convertScaleAbs(grad_x)
    abs_y = cv2.convertScaleAbs(grad_y)

    # API 融合：快速观察综合边缘
    edge_add = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)

    # 公式融合：G = sqrt(Gx^2 + Gy^2)
    edge_magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
    edge_magnitude = cv2.normalize(edge_magnitude, None, 0, 255, cv2.NORM_MINMAX)
    edge_magnitude = edge_magnitude.astype(np.uint8)

    return abs_x, abs_y, edge_add, edge_magnitude


def laplacian_demo(image, ksize=3, sharpen_strength=0.7):
    """
    Laplacian 算子演示：边缘检测 + 图像锐化。

    cv2.Laplacian(src, ddepth, ksize)
    src: 输入灰度图
    ddepth: 输出数据类型。使用 cv2.CV_64F，防止负值被 uint8 截断
    ksize: 卷积核大小，常用 1、3、5，必须是正奇数

    sharpen_strength: 锐化强度，越大边缘增强越明显，但过大会产生噪声和白边
    """
    # Laplacian 是二阶导数，输出可能有正有负，所以先用 float64 保存
    lap = cv2.Laplacian(image, cv2.CV_64F, ksize=ksize)

    # 边缘检测显示：取绝对值并转回 uint8
    edge = cv2.convertScaleAbs(lap)

    # 图像锐化：
    # 如果 lap 是二阶边缘信息，原图减去一部分 lap 可以增强边缘和细节。
    # 这里要先把 image 转成 float64，否则 uint8 直接相减容易溢出或截断。
    sharpened = image.astype(np.float64) - sharpen_strength * lap

    # 锐化结果要限制到 [0,255]，再转回 uint8 才能正常显示
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)

    return edge, sharpened


def canny_demo(image, threshold1=25, threshold2=120, aperture_size=3):
    """
    Canny 边缘检测演示。

    cv2.Canny(image, threshold1, threshold2, apertureSize)
    image: 输入灰度图，通常建议先高斯滤波
    threshold1: 低阈值，小于它的边缘一般会被丢弃
    threshold2: 高阈值，大于它的边缘会被认为是强边缘
    apertureSize: Sobel 算子的卷积核大小，常用 3、5、7

    阈值理解：
    threshold2 越大，保留下来的强边缘越少。
    threshold1 越小，越容易连接弱边缘，但也可能引入噪声。
    常见经验：threshold2 约为 threshold1 的 2 倍或 3 倍。
    """
    edge = cv2.Canny(
        image=image,
        threshold1=threshold1,
        threshold2=threshold2,
        apertureSize=aperture_size
    )
    return edge


if __name__ == "__main__":
    img_path = "arknights.jpg"

    # 直接读取灰度图，结果是二维 numpy 数组
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img_gray is None:
        print("图片路径错误，请检查 img_path")
        exit()

    print("shape:", img_gray.shape)
    print("dtype:", img_gray.dtype)
    print("min/max:", img_gray.min(), img_gray.max())

    # 可选：先高斯滤波，减少噪声对边缘检测的干扰
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), sigmaX=0)

    sobel_x, sobel_y, sobel_add, sobel_mag = sobel_demo(img_blur, ksize=3)
    scharr_x, scharr_y, scharr_add, scharr_mag = scharr_demo(img_blur)
    lap_edge, lap_sharp = laplacian_demo(img_blur, ksize=3, sharpen_strength=0.7)
    canny_edge = canny_demo(img_blur, threshold1=35, threshold2=160, aperture_size=3)

    cv2.imwrite("./output/sobel.jpg",sobel_add)
    cv2.imwrite("./output/scharr.jpg",scharr_add)
    cv2.imwrite("./output/laplacian.jpg",lap_edge)
    cv2.imwrite("./output/canny.jpg",255-canny_edge)

    # show_images(
    #     [img_gray, img_blur, sobel_x, sobel_y, sobel_add, sobel_mag],
    #     ["Original", "Gaussian Blur", "Sobel X", "Sobel Y", "Sobel X + Y", "Sobel Magnitude"]
    # )
    #
    # show_images(
    #     [img_gray, img_blur, scharr_x, scharr_y, scharr_add, scharr_mag],
    #     ["Original", "Gaussian Blur", "Scharr X", "Scharr Y", "Scharr X + Y", "Scharr Magnitude"]
    # )
    #
    # show_images(
    #     [sobel_add, scharr_add, sobel_mag, scharr_mag],
    #     ["Sobel X + Y", "Scharr X + Y", "Sobel Magnitude", "Scharr Magnitude"]
    # )
    #
    # show_images(
    #     [img_gray, img_blur, lap_edge, lap_sharp],
    #     ["Original", "Gaussian Blur", "Laplacian Edge", "Laplacian Sharpen"]
    # )
    #
    # show_images(
    #     [sobel_add, scharr_add, lap_edge, canny_edge],
    #     ["Sobel", "Scharr", "Laplacian", "Canny"]
    # )
