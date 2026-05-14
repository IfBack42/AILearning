"""
基础的图像操作：绘制、加载、保存

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
import torch
import matplotlib.pyplot as plt
import numpy as np

# 绘制全黑全白图
def draw():
    # 定义全黑图：0-255，值越小越黑、越大越白
    # HWC: H高、W宽、C通道 通道在哪儿具体看框架需求
    img1 = np.zeros((200,200,3))
    # print(f"img1:{img1.shape}")

    # 绘制图片
    plt.imshow(img1)
    plt.axis('off')
    plt.show()

    # 定义全白图片
    img2 = np.full(shape=(200,200,3),fill_value=233)
    # print(f"img2:{img2.shape}")

    # 绘制图片
    plt.imshow(img2)
    plt.show()

# 加载图片
def img_load():
    # 加载图片
    img = plt.imread('./data/img.png')
    # 绘制图片
    plt.imshow(img)
    plt.show()
    # 图片保存
    plt.imsave('./data/img_save.png',img)

if __name__ == '__main__':
    # draw()
    img_load()