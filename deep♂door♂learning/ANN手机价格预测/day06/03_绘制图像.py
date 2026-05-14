"""
案例:
    演示基础的图像操作.

图像分类:
    二值图:        1通道, 每个像素点由0, 1组成
    灰度图:        1通道, 每个像素点的范围: [0, 255]
    索引图:        1通道, 每个像素点的范围: [0, 255], 像素点表示颜色表的索引
    RGB真彩图:     3通道, Red, Green, Blue, 红绿蓝.

涉及到的API:
    imshow()    基于HWC, 展示图像
    imread()    读取图像, 获取HWC
    imsave()    基于HWC, 保存图片.
"""

# 导包
import numpy as np
import matplotlib.pyplot as plt
import torch

# 1. 定义函数, 绘制: 全黑, 全白图.
def dm01():
    # 1. 定义全黑图片: 像素点越接近0越黑, 越接近255越白.
    # HWC:  H: 高度, W: 宽度, C: 通道.
    img1 = np.zeros((200, 200, 3))
    # print(f'img1: {img1}')

    # 2. 绘制图片.
    plt.imshow(img1)
    # plt.axis('off')
    plt.show()

    # 2. 定义全白图片.
    img2 = torch.full(size=(200, 200, 3), fill_value=255)
    # print(f'img2: {img2}')
    plt.imshow(img2)
    # plt.axis('off')
    plt.show()

# 2. 定义函数, 加载图片.
def dm02():
    # 1. 加载图片.
    img1 = plt.imread('./data/img.jpg')
    # print(f'img1: {img1}')
    # print(f'img1.shape: {img1.shape}')  # (640, 640, 3), HWC

    # 2. 保存图像.
    plt.imsave('./data/img_copy.png', img1)

    # 3. 展示图像.
    plt.imshow(img1)
    plt.show()


# 3. 测试
if __name__ == '__main__':
    # dm01()
    dm02()