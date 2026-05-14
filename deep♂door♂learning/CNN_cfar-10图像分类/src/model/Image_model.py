"""
CNN的综合案例, 图像分类.

深度学习项目的步骤:
    1. 准备数据集.
        这里我们用的时候 计算机视觉模块 torchvision自带的 CIFAR10数据集, 包含6W张 (32,32,3)的图片, 5W张训练集, 1W张测试集, 10个分类, 每个分类6K张图片.
        你需要单独安装一下 torchvision包, 即: pip install torchvision
    2. 搭建(卷积)神经网络
    3. 模型训练.
    4. 模型测试.

卷积层:
    提取图像的局部特征 -> 特征图(Feature Map), 计算方式:  N = (W - F + 2P) // S + 1
    每个卷积核都是1个神经元.

池化层:
    降维, 有最大池化 和 平均池化.
    池化只在HW上做调整, 通道上不改变.

案例的优化思路:
    1. 增加卷积核的输出通道数(大白话: 卷积核的数量)
    2. 增加全连接层的参数量.
    3. 调整学习率
    4. 调整优化方法(optimizer...)
    5. 调整激活函数...
    6. ...
"""

import torch
import torch.nn as nn
import torchsummary
from torch.nn.functional import dropout

Dropout_rate = 0.5

class Image_model(nn.Module):
    def __init__(self,input_dim,n_class):
        super().__init__()
        # 创建卷积层
        # Sequential 是 PyTorch 中的一个容器模块，用于按顺序组织多个神经网络层,会自动将前一层的输出作为后一层的输入
        self.conv = nn.Sequential(
            # 第1层：64x64 -> 32x32
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 64x64 -> 32x32

            # 第2层：32x32 -> 16x16
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 32x32 -> 16x16

            # 第3层：16x16 -> 8x8
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 16x16 -> 8x8

            # 自适应池化到4x4（避免尺寸过小）
            nn.AdaptiveAvgPool2d((4, 4))
        )
        """
            尝试了很多 线性层输入动态适应 的方法，
            只要涉及到层初始化就很难提前预知卷积层展平大小，
            查过后发现使用 自适应池化AdaptiveAvgPool2d 是最常用方法
        """

        # 创建全连接层
        self.fc = nn.Sequential(
            nn.Linear(256 * 4 * 4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(512, n_class)
        )


    def forward(self,x):
        x = self.conv(x)
        x = x.view(x.size(0),-1)
        # print(x.size())
        out_put = self.fc(x)
        return out_put

if __name__ == '__main__':
    model = Image_model(3,10)
    torchsummary.summary(model,(3,64,64),batch_size=1)
    print(model)