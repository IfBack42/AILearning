import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
img_path = "2.jpg"
img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# 判断是否读取成功
if img_gray is None:
    print("图像读取失败")
    exit()


# 计算灰度直方图
hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])

# 显示灰度图
cv2.imshow("Gray Image", img_gray)

# 绘制直方图
plt.figure("Gray Histogram")
plt.title("Gray Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Count")
plt.plot(hist)
plt.xlim([0, 256])

# 显示窗口
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()