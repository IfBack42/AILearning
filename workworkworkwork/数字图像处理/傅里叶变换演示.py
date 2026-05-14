import cv2
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------
# 1. 显示原图及其频谱（让你看看频率域长什么样）
# ----------------------------------------------
def show_spectrum(image_path):
    # 读图并转为灰度
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("图片路径错误，请检查")
        return

    # 傅里叶变换
    f = np.fft.fft2(img)  # 二维FFT
    fshift = np.fft.fftshift(f)  # 低频移到中心
    magnitude = np.log(1 + np.abs(fshift))  # 取幅度并压缩显示范围

    # 画图
    plt.figure(figsize=(10, 5))
    plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Original Image')
    plt.subplot(122), plt.imshow(magnitude, cmap='gray'), plt.title('Frequency Spectrum (center = low freq)')
    plt.show()


# ----------------------------------------------
# 2. 低通滤波实验：只保留中心低频，去掉高频
#    效果：图像模糊，但整体轮廓保留
# ----------------------------------------------
def lowpass_filter(image_path, radius=30):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("图片路径错误")
        return

    # 傅里叶变换
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # 生成低通掩膜：中心一个圆内为1，其余为0
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols), np.uint8)
    cv2.circle(mask, (ccol, crow), radius, 1, -1)  # 白色圆形区域=低频保留

    # 应用掩膜（频域乘法）
    fshift_filtered = fshift * mask
    # 逆变换回空间域
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_filtered = np.abs(np.fft.ifft2(f_ishift))

    # 显示结果
    plt.figure(figsize=(12, 4))
    plt.subplot(131), plt.imshow(img, cmap='gray'), plt.title('Original')
    plt.subplot(132), plt.imshow(mask, cmap='gray'), plt.title('Lowpass Mask (white=keep)')
    plt.subplot(133), plt.imshow(img_filtered, cmap='gray'), plt.title(f'Lowpass Result (radius={radius})')
    plt.show()


# ----------------------------------------------
# 3. 高通滤波实验：只保留高频，去掉中心低频部分
#    效果：只剩边缘、纹理、噪声
# ----------------------------------------------
def highpass_filter(image_path, radius=30):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("图片路径错误")
        return

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # 生成高通掩膜：中心圆内为0，其余为1（与低通相反）
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols), np.uint8)
    cv2.circle(mask, (ccol, crow), radius, 0, -1)  # 中心圆形区域设为0（去掉低频）

    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_filtered = np.abs(np.fft.ifft2(f_ishift))

    # 显示
    plt.figure(figsize=(12, 4))
    plt.subplot(131), plt.imshow(img, cmap='gray'), plt.title('Original')
    plt.subplot(132), plt.imshow(mask, cmap='gray'), plt.title('Highpass Mask (black=removed)')
    plt.subplot(133), plt.imshow(img_filtered, cmap='gray'), plt.title(f'Highpass Result (radius={radius})')
    plt.show()


# ----------------------------------------------
# 额外：能量集中展示（自动计算低频圆内能量占比）
# 不需要你改代码，直接运行会打印百分比
# ----------------------------------------------
def energy_concentration(image_path, radius=30):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("图片路径错误")
        return

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    energy = np.abs(fshift) ** 2  # 每个频率分量的能量

    total_energy = np.sum(energy)

    # 计算半径为radius的圆内能量
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    mask_circle = (x - ccol) ** 2 + (y - crow) ** 2 <= radius ** 2
    energy_in_circle = np.sum(energy[mask_circle])

    percent = 100 * energy_in_circle / total_energy
    print(f"半径为 {radius} 像素的低频圆内包含的能量占总能量的比例: {percent:.2f}%")

    # 显示低频频谱区域（白色部分）
    plt.imshow(mask_circle, cmap='gray')
    plt.title(f"Low-frequency region (radius={radius})")
    plt.show()


# ==============================================
# 如何使用：
# 1. 把下面的 'your_image.jpg' 换成你自己的图片路径
# 2. 依次调用函数，观察结果
# ==============================================
if __name__ == "__main__":
    image_path = "naixu.jpg"  # <--- 改成你的图片路径

    # 实验1：先看频谱
    show_spectrum(image_path)

    # 实验2：低通滤波（试着改 radius = 10, 50，看模糊程度变化）
    lowpass_filter(image_path, radius=30)

    # 实验3：高通滤波（边缘提取效果）
    highpass_filter(image_path, radius=30)

    # 实验4：看能量集中程度
    energy_concentration(image_path, radius=30)