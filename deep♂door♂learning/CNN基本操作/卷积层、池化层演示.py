"""
演示卷积层的API, 用于 提取图像的局部特征, 获取: 特征图(Feature Map)

卷积神经网络介绍:
    概述:
        全称叫: Convolutional neural network, 即: 包含卷积层的神经网络.
    组成:
        卷积层(Convolutional):
            用于提取图像的 局部特征, 结合 卷积核(每个卷积核 = 1个神经元) 实现, 处理后的结果叫: 特征图.

        批量归一化(Batch Normalization):
            作用：对每一批数据进行标准化处理
            原理：将每一层的输入分布规范化为均值为0、方差为1的标准正态分布
            优势：加快训练速度，允许使用更高的学习率
                 减少对初始化的敏感性
                 具有一定的正则化效果

        Relu激活函数:
            优点：计算简单，梯度不会饱和
                 缓解梯度消失问题
                 提高模型的表达能力

        池化层(Pooling):
            目的:
                降维.
            思路:
                最大池化.
                平均池化.
            特点:
                池化不会改变数据的 通道数.
            用于 降维, 降采样

        全连接层(Full Connected, fc, linear):
            用于 预测结果, 并输出结果的.

    特征图计算方式:
        N = (W - F + 2*P) / S   +  1
        W: 输入图像的大小
        F: 卷积核的大小
        P: 填充的大小
        S: 步长
        N: 输出图像的大小(特征图大小)


"""

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

def conv_demo():
    # 1.卷积前的图像数据处理
    # 加载图片
    img = plt.imread('./data/img.png') # (252, 281, 3)
    print(f'shape: {img.shape}')

    # 先转换图像为张量、再转换图像通道为CHW
    img = torch.tensor(img,dtype=torch.float)
    img = img.permute(2,0,1)
    # img = torch.permute(img,(2,0,1))
    print(f'shape: {img.shape}') # ([3, 252, 281])

    # 增维，增加图像每批个数维度
    img.unsqueeze_(dim=0) # ([1, 3, 252, 281])
    print(f'shape: {img.shape}')

    # 2.正式的卷积
    # 创建卷积层       输入通道      输出通道      卷积核大小    步长     填充
    conv = nn.Conv2d(3,4,3,1,0)
    conved_img = conv(img)
    print(f'shape: {conved_img.shape}') # ([1, 4, 250, 279])

    # 查看合并后特征图（先转换维度）
    conved_img1 = conved_img[0].permute(1,2,0) # ([250, 279, 4])
    print(f'shape: {conved_img1.shape}')
    plt.imshow(conved_img1.detach().numpy())
    plt.show()

    # 分别查看4张特征图
    for i in range(conved_img.shape[1]):
        show_img = conved_img1[:,:,i]
        plt.imshow(show_img.detach().numpy())
        plt.show()

def single_pooling():
    # 创建单通道二维矩阵示例数据
    input = torch.tensor([  # 通道 C
        [                   # 高度 H
            [1,1,4],        # 宽度 W
            [5,1,4],
            [1,9,1]
        ]
    ])
    # 最大池化层           窗口大小     步长    填充
    pool1 = nn.MaxPool2d(2,1,0)
    output1 = pool1(input)
    print(f'output: {output1},\n shape: {output1.shape}')

    # 平均池化层
    pool2 = nn.AvgPool2d(2,1,0)
    output2 = pool2(input)
    print(f'output: {output2},\n shape: {output2.shape}')

def multi_pooling():
    # 创建多通道二维矩阵示例数据
    input = torch.tensor([ # 通道 C
        [                  # 通道1的高度 H
            [1,1,4],       # 宽度 W
            [5,1,4],
            [1,9,1]
        ],
        [
            [9,8,1],
            [0,1,1],
            [4,5,1]
        ],
        [
            [4,1,9],
            [1,9,8],
            [1,0,1]
        ]
    ])

    # 创建多通道池化层
    multi_pool1 = nn.MaxPool2d(2,1,0)
    output1 = multi_pool1(input)
    print(f'output: {output1},\n shape: {output1.shape}')

    multi_pool2 = nn.AvgPool2d(2,1,0)
    output2 = multi_pool2(input)
    print(f'output: {output2},\n shape: {output2.shape}')



if __name__ == '__main__':
    # conv_demo()
    # single_pooling()
    multi_pooling()