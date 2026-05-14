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
# 以下三个函数用于去噪演示，调用前需要先施加椒盐噪声
# ==============================================

# 椒盐噪声攻击函数
def salt_pepper_noise(image, prob=0.02):
    """
    添加椒盐噪声
    prob: 噪声比例（每个像素被替换为椒或盐的概率）
    """
    output = image.copy()
    # 椒盐噪声：随机将一些像素设成 0（胡椒）或 255（盐）
    rand = np.random.rand(*image.shape)
    output[rand < prob/2] = 0
    output[rand > 1 - prob/2] = 255
    return output

# 高斯噪声攻击函数
def gaussian_noise(image, mean=0, sigma=25):
    """
    添加高斯噪声
    mean: 噪声均值
    sigma: 噪声标准差，控制噪声强度
    """
    output = image.astype(np.float64)
    # 生成高斯噪声
    noise = np.random.normal(mean, sigma, image.shape)
    # 添加噪声并裁剪到 [0, 255]
    noisy = output + noise
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    return noisy

# 3. 均值滤波（平滑去噪）
def mean_filter(image, ksize=3):
    """
    均值滤波：用窗口内所有像素的平均值替代中心像素。
    优点：简单、快速；缺点：模糊边缘。
    适用：高斯噪声、轻度颗粒噪声。
    """
    return cv2.blur(image, (ksize, ksize))

# 4. 中值滤波（保护边缘的去噪）
def median_filter(image, ksize=3):
    """
    中值滤波：用窗口内所有像素的中位数替代中心像素。
    优点：对椒盐噪声效果极好，且几乎不模糊边缘。
    缺点：对高斯噪声效果不如均值滤波。
    """
    return cv2.medianBlur(image, ksize)

# 5. 高斯滤波（保留边缘的平滑）
def gaussian_filter(image, ksize=3, sigma=0):
    """
    高斯滤波：根据高斯函数给邻域像素加权平均，中心权重大，边缘权重小。
    优点：平滑噪声的同时，比均值滤波更保留边缘。
    适用：高斯噪声（常见于低光照图像）。
    """
    return cv2.GaussianBlur(image, (ksize, ksize), sigma)

# ==============================================
# 主程序：依次演示每个功能
# ==============================================
if __name__ == "__main__":

    img_path = "naixu.jpg"
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        print("图片路径错误，请检查")
        exit()

    # ==========================================
    # 演示1：椒盐噪声 + 三种滤波对比
    # ==========================================
    noisy_sp = salt_pepper_noise(img_gray, prob=0.05)

    mean_sp = mean_filter(noisy_sp, ksize=3)
    median_sp = median_filter(noisy_sp, ksize=3)
    gaussian_sp = gaussian_filter(noisy_sp, ksize=3, sigma=1)

    plt.figure(figsize=(16, 8))
    plt.subplot(241), plt.imshow(img_gray, cmap='gray'), plt.title("Original")
    plt.subplot(242), plt.imshow(noisy_sp, cmap='gray'), plt.title("Salt-Pepper Noise")
    plt.subplot(243), plt.imshow(mean_sp, cmap='gray'), plt.title("Mean Filter")
    plt.subplot(244), plt.imshow(median_sp, cmap='gray'), plt.title("Median Filter (Best)")
    plt.subplot(245), plt.imshow(gaussian_sp, cmap='gray'), plt.title("Gaussian Filter")
    plt.tight_layout()
    plt.show()

    # ==========================================
    # 演示2：高斯噪声 + 三种滤波对比
    # ==========================================
    noisy_gauss = gaussian_noise(img_gray, mean=0, sigma=25)

    mean_gauss = mean_filter(noisy_gauss, ksize=5)
    median_gauss = median_filter(noisy_gauss, ksize=5)
    gaussian_gauss = gaussian_filter(noisy_gauss, ksize=5, sigma=1)

    plt.figure(figsize=(16, 8))
    plt.subplot(241), plt.imshow(img_gray, cmap='gray'), plt.title("Original")
    plt.subplot(242), plt.imshow(noisy_gauss, cmap='gray'), plt.title("Gaussian Noise")
    plt.subplot(243), plt.imshow(mean_gauss, cmap='gray'), plt.title("Mean Filter")
    plt.subplot(244), plt.imshow(median_gauss, cmap='gray'), plt.title("Median Filter")
    plt.subplot(245), plt.imshow(gaussian_gauss, cmap='gray'), plt.title("Gaussian Filter")
    plt.tight_layout()
    plt.show()