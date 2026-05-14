"""
正则化的作用:
    缓解模型的过拟合情况.

正则化的方式:
    L1正则化: 权重可以变为0, 相当于: 降维.
    L2正则化: 权重可以无限接近0
    DropOut: 随机失活, 每批次样本训练时, 随机让一部分神经元死亡, 防止一些特征对结果的影响较大(防止过拟合)
    BN(批量归一化): ...

随机失活：
    训练阶段
        前向传播：
            保留所有神经元参与计算
            以概率 p 随机将部分神经元输出置为 0
            对剩余神经元进行缩放：output = input * mask / (1-p)
        反向传播：
            使用相同的 mask 掩码
            只有未被置零的神经元参与梯度传播
    推理阶段
        前向传播：
            所有神经元参与计算
            不应用任何随机失活
            不进行额外缩放（因为训练时已经进行了缩放）

批量归一化：
    也属于正则化的一种, 也是用于 缓解模型的 过拟合情况的.

    思路:
        先对数据做标准化(会丢失一些信息), 然后再对数据做 缩放(λ, 理解为: w权重) 和 平移(β, 理解为: b偏置), 再找补回一些信息.
    应用场景:
        批量归一化在计算机视觉领域使用较多.











        BatchNorm1d：主要应用于全连接层或处理一维数据的网络，例如文本处理。它接收形状为 (N, num_features) 的张量作为输入。
        BatchNorm2d：主要应用于卷积神经网络，处理二维图像数据或特征图。它接收形状为 (N, C, H, W) 的张量作为输入。
        BatchNorm3d：主要用于三维卷积神经网络 (3D CNN)，处理三维数据，例如视频或医学图像。它接收形状为 (N, C, D, H, W) 的张量作为输入。
"""

import torch
import torch.nn as nn

# 随机失活
def dropout():
    # 创建隐藏层输出结果
    t1 = torch.randn(size=(1,5))
    print(f't1:{t1.data}')
    # 创建线性层
    l1 = nn.Linear(5,4)
    # print(l1.weight,l1.bias) # 创建线性层自动使用了kaiming初始化
    t1 = l1(t1)
    print(f't1:{t1.data}')
    # 创建激活函数
    r1 = nn.ReLU()
    t1 = r1(t1)
    print(f't1:{t1.data}')

     # 创建随机失活层
    d1 = nn.Dropout(p=0.5)
    t1 = d1(t1)
    print(f't1:{t1.data}')

# 批量归一化处理一维数据
def one_dimension():
    # 创建样本数据
    t2 = torch.randn(size=(2,2))
    print(f't2:{t2.data}')
    # 创建线性层
    l2 = nn.Linear(2,4)
    t2 = l2(t2)
    print(f't2:{t2.data}')

    # 创建批量归一化层
    bn1d = nn.BatchNorm1d(num_features=4)
    t2 = bn1d(t2)
    print(f't2:{t2.data}')

# 批量归一化处理二维数据
def two_dimension():
    # 创建图像样本数据 1张图片、2通道、3*4像素
    t3 = torch.randn(size=(1,2,3,4))
    print(f't3:{t3.data}')

    # 创建批量归一化层
    # 参1: 输入特征数 = 图片的通道数.
    # 参2: 噪声值(小常数), 默认为1e-5.
    # 参3: 动量值, 用于计算移动平局统计量的  动量值.
    # 参4: 表示使用可学习的变换参数(λ, β) 对归一化(标准化)后的数据进行 缩放和平移.
    bn2d = nn.BatchNorm2d(num_features=2, eps=1e-5, momentum=0.1, affine=True)
    t3 = bn2d(t3)
    print(f't3:{t3.data}')

if __name__ == '__main__':
    # dropout()
    # one_dimension()
    two_dimension()