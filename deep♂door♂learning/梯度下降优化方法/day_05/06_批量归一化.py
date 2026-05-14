"""
案例:
    代码演示批量归一化,  它(批量归一化)也属于正则化的一种, 也是用于 缓解模型的 过拟合情况的.

批量归一化:
    思路:
        先对数据做标准化(会丢失一些信息), 然后再对数据做 缩放(λ, 理解为: w权重) 和 平移(β, 理解为: b偏置), 再找补回一些信息.
    应用场景:
        批量归一化在计算机视觉领域使用较多.

        BatchNorm1d：主要应用于全连接层或处理一维数据的网络，例如文本处理。它接收形状为 (N, num_features) 的张量作为输入。
        BatchNorm2d：主要应用于卷积神经网络，处理二维图像数据或特征图。它接收形状为 (N, C, H, W) 的张量作为输入。
        BatchNorm3d：主要用于三维卷积神经网络 (3D CNN)，处理三维数据，例如视频或医学图像。它接收形状为 (N, C, D, H, W) 的张量作为输入。
"""

# 导包
import torch
import torch.nn as nn


# 1. 定义函数, 处理 二维数据.
def dm01():
    # 1. 创建图像样本数据.
    # 1张图片, 2个通道, 3行4列(像素点)
    input_2d = torch.randn(size=(1, 2, 3, 4))
    print(f'input_2d: {input_2d}')

    # 2. 创建批量归一化层(BN层)
    # 参1: 输入特征数 = 图片的通道数.
    # 参2: 噪声值(小常数), 默认为1e-5.
    # 参3: 动量值, 用于计算移动平局统计量的  动量值.
    # 参4: 表示使用可学习的变换参数(λ, β) 对归一化(标准化)后的数据进行 缩放和平移.
    bn2d = nn.BatchNorm2d(num_features=2, eps=1e-5, momentum=0.1, affine=True)

    # 3. 对数据进行 批量归一化处理.
    output_2d = bn2d(input_2d)
    print(f'output_2d: {output_2d}')


# 2. 定义函数, 处理: 一维数据.
def dm02():
    # 1. 创建样本数据.
    # 2行2列, 2条样本, 每个样本有2个特征
    input_1d = torch.randn(size=(2, 2))
    print(f'input_1d: {input_1d}')

    # 2. 创建线性层.
    linear1 = nn.Linear(2, 4)

    # 3. 对数据进行 线性变换.
    l1 = linear1(input_1d)
    print(f'l1: {l1}')

    # 4. 创建批量归一化层.
    bn1d = nn.BatchNorm1d(num_features=4)
    # 5. 对线性处理结果l1 进行 批量归一化处理.
    output_1d = bn1d(l1)
    print(f'output_1d: {output_1d}')



# 3. 测试
if __name__ == '__main__':
    dm01()
    # dm02()