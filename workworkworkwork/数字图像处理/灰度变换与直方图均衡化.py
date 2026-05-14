import cv2
import numpy as np
import matplotlib.pyplot as plt

# ==============================================
# 辅助函数：显示原图和处理结果
# ==============================================
def show_images(original, processed, title1="Original", title2="Processed"):
    plt.figure(figsize=(10,5))
    plt.subplot(121), plt.imshow(original, cmap='gray'), plt.title(title1)
    plt.subplot(122), plt.imshow(processed, cmap='gray'), plt.title(title2)
    plt.show()

# ==============================================
# 1. 灰度线性变换（对比度拉伸）
# 公式：s = c + (d-c)/(b-a) * (r - a)
# 作用：将原图灰度范围 [a,b] 拉伸到 [c,d]，增强中间区域对比度
# ==============================================
def linear_stretch(image, a, b, c, d):
    """
    image: 灰度图 (0-255)
    a, b: 原图中要拉伸的灰度范围（通常是 min, max 或者自定义）
    c, d: 目标灰度范围
    """
    # 确保图像是 float 类型，避免溢出
    img_float = image.astype(np.float32)
    # 线性映射
    stretched = c + (d - c) / (b - a) * (img_float - a)
    # 裁剪到 [0,255] 并转成 uint8
    stretched = np.clip(stretched, 0, 255).astype(np.uint8)
    return stretched

# ==============================================
# 2. 直方图均衡化（自动增强对比度）
# 原理：重新映射灰度，使输出直方图近似均匀分布
# 作用：对光照不均、整体偏暗或偏亮的图效果明显
# ==============================================
def histogram_equalize(image):
    # OpenCV 提供的直方图均衡化（自动处理）
    return cv2.equalizeHist(image)

# ==============================================
# 灰度反转（黑白反相）
# 公式：s = 255 - r
# 作用：把亮的地方变暗，把暗的地方变亮
# ==============================================
def gray_invert(image):
    """
    image: 灰度图，通常是 uint8，像素范围 [0, 255]
    返回值: 灰度反转后的图像

    0 会变成 255，255 会变成 0。
    对 uint8 灰度图，可以直接用 255 - image。
    """
    return 255 - image

# 3. 绘制图像直方图分布
# 作用：可视化图像灰度值的统计分布情况
# ==============================================
def plot_histogram(image, title="Histogram"):
    """
    image: 灰度图 (0-255)
    title: 图表标题
    """
    # 计算直方图：256个灰度级，范围0-255
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    # 绘制直方图
    plt.figure(figsize=(10, 4))
    plt.plot(hist, color='black')
    plt.xlim([0, 256])
    plt.xlabel('Pixel Value (0-255)')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.grid(alpha=0.3)
    plt.show()

# ==============================================
# 主程序：依次演示每个功能
# ==============================================
if __name__ == "__main__":
    # 请修改成你自己的图片路径
    img_path = "save.jpg"
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        print("图片路径错误，请检查")
        exit()

    # ---------- 演示1：灰度线性变换 ----------
    # 参数：原图灰度范围 [40, 200] 拉伸到 [20, 235]
    stretched = linear_stretch(img_gray, a=40, b=200, c=20, d=235)
    show_images(img_gray, stretched, "Original", "Linear Stretch (40→20, 200→235)")

    # ---------- 演示2：灰度反转 ----------
    inverted = gray_invert(img_gray)
    show_images(img_gray, inverted, "Original", "Gray Invert")
    cv2.imwrite("save.jpg",inverted)

    # ---------- 演示3：直方图均衡化 ----------
    equalized = histogram_equalize(img_gray)
    show_images(img_gray, equalized, "Original", "Histogram Equalization")

    # ---------- 演示4：绘制直方图分布 ----------
    plot_histogram(img_gray, "Original Image Histogram")
    plot_histogram(inverted, "Gray Invert Histogram")
    plot_histogram(equalized, "Equalized Image Histogram")
    plot_histogram(stretched, "Equalized Image Linear Stretch")
