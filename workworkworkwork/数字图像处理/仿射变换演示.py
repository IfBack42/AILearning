import cv2
import numpy as np
import matplotlib.pyplot as plt

# ==============================================
# 仿射变换快速复习
# ==============================================
# 仿射变换作用：平移、缩放、旋转、剪切、反射，以及它们的组合。
#
# OpenCV 中仿射矩阵是 2x3：
# [ a  b  tx ]
# [ c  d  ty ]
#
# 对任意像素点 (x, y)，变换公式是：
# x' = a*x + b*y + tx
# y' = c*x + d*y + ty
#
# 其中：
# a, b, c, d：控制旋转、缩放、剪切、反射
# tx, ty：控制平移，tx 向右为正，ty 向下为正
#
# 常用 API：
# cv2.warpAffine(src, M, dsize)
# src: 输入图像
# M: 2x3 仿射矩阵，建议使用 np.float32
# dsize: 输出图像大小，格式是 (width, height)，也就是 (cols, rows)


def show_images(images, titles):
    """并排显示多张图像。"""
    plt.figure(figsize=(5 * len(images), 7))
    for i, (image, title) in enumerate(zip(images, titles), start=1):
        plt.subplot(1, len(images), i)
        plt.imshow(image)
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()
    plt.show()


def transform_points(points, M):
    """
    手动计算点坐标的仿射变换，用来理解矩阵含义。

    points: 原始点坐标，形状为 (N, 2)，每一行是 [x, y]
    M: 2x3 仿射矩阵
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

    image: RGB 图像
    M: 2x3 仿射矩阵，必须能转换为 np.float32
    """
    rows, cols = image.shape[:2]

    # OpenCV 要求仿射矩阵是 2x3，常用 float32 格式。
    M = np.float32(M)

    # dsize 是输出图像大小，注意顺序是 (宽, 高)，不是 (高, 宽)。
    result = cv2.warpAffine(image, M, dsize=(cols, rows))
    return result


def get_translate_matrix(tx, ty):
    """平移矩阵：tx 向右，ty 向下。"""
    return np.float32([
        [1, 0, tx],
        [0, 1, ty]
    ])


def get_rotate_matrix(image, angle, scale=1.0):
    """
    旋转矩阵。

    angle: 旋转角度，正数表示逆时针
    scale: 缩放比例，1.0 表示原大小

    cv2.getRotationMatrix2D(center, angle, scale)
    center: 旋转中心，通常取图像中心点
    """
    rows, cols = image.shape[:2]
    center = (cols / 2, rows / 2)
    return cv2.getRotationMatrix2D(center, angle, scale)


def get_reflect_x_matrix(image):
    """
    水平反射/左右镜像矩阵。

    x' = -x + (cols - 1)
    y' = y

    这是仿射变换的一个特殊例子。
    """
    rows, cols = image.shape[:2]
    return np.float32([
        [-1, 0, cols - 1],
        [0, 1, 0]
    ])


def get_three_points_matrix():
    """
    三点确定仿射变换。

    cv2.getAffineTransform(src, dst)
    src: 原图上的 3 个点，形状是 (3, 2)，float32
    dst: 目标图上的 3 个点，形状是 (3, 2)，float32

    只要知道 3 个点变换前后的位置，OpenCV 就能反推出 2x3 矩阵。
    """
    src = np.float32([
        [50, 50],
        [200, 50],
        [50, 200]
    ])

    dst = np.float32([
        [30, 80],
        [220, 40],
        [80, 230]
    ])

    return cv2.getAffineTransform(src, dst)


if __name__ == "__main__":
    image_path = "naixu.jpg"

    # OpenCV 默认读取 BGR，Matplotlib 显示要转成 RGB。
    img_bgr = cv2.imread(image_path)

    if img_bgr is None:
        print("图片路径错误，请检查 image_path")
        exit()

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    print("image shape:", img_rgb.shape)
    print("image dtype:", img_rgb.dtype)

    # ==========================================
    # 1. 点坐标变换：理解矩阵公式
    # ==========================================
    M_demo = np.float32([
        [1, 0.2, 100],
        [0.2, 1, 50]
    ])

    points_old = np.float32([
        [0, 0],
        [10, 0],
        [0, 10]
    ])

    points_new = transform_points(points_old, M_demo)
    print("原始点:\n", points_old)
    print("变换矩阵 M:\n", M_demo)
    print("变换后的点:\n", points_new)

    # OpenCV 验证：cv2.transform 的点格式需要是 (N, 1, 2)。
    points_cv = points_old.reshape(-1, 1, 2)
    points_cv_new = cv2.transform(points_cv, M_demo).reshape(-1, 2)
    print("OpenCV 验证结果:\n", points_cv_new)

    # ==========================================
    # 2. 图像仿射变换演示
    # ==========================================
    M_translate = get_translate_matrix(tx=80, ty=40)
    M_rotate = get_rotate_matrix(img_rgb, angle=30, scale=1.0)
    M_reflect = get_reflect_x_matrix(img_rgb)
    M_three_points = get_three_points_matrix()

    img_translate = apply_affine(img_rgb, M_translate)
    img_rotate = apply_affine(img_rgb, M_rotate)
    img_reflect = apply_affine(img_rgb, M_reflect)
    img_three_points = apply_affine(img_rgb, M_three_points)

    show_images(
        [img_rgb, img_translate, img_rotate],
        ["Original", "Translate", "Rotate"]
    )

    show_images(
        [img_rgb, img_reflect, img_three_points],
        ["Original", "Reflect X", "3 Points Affine"]
    )
