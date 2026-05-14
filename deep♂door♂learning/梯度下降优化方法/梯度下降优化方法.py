"""
梯度下降优化方法.

梯度下降相关介绍:
    概述:
        梯度下降是结合 本次损失函数的导数(作为梯度) 和 学习率 来更新权重的.
    公式:
        W新 = W旧 - 学习率 * (本次的)梯度
    存在的问题:
        1. 遇到平缓区域, 梯度下降(权重更新)可能会慢.
        2. 可能会遇到 鞍点(梯度为0)
        3. 可能会遇到 局部最小值.
        4. 遇到断崖,跳崖式快速更新错过最优点
        5. 最优点附近反复横跳收敛过慢
    解决思路:
        从上述的 学习率 或者 梯度入手, 进行优化, 于是有了: 动量法Momentum, 自适应学习率AdaGrad, RMSProp, 综合衡量: Adam

    动量法Momentum:
        动量法公式:
            St = β * St-1 + (1 - β) * Gt
        解释:
            St:     本次的指数移动加权平均结果.
            β:      调节权重系数, 越大, 数据越平缓, 历史指数移动加权平均 比重越大, 本次梯度权重越小.
            St-1:   历史的指数移动加权平均结果.
            Gt:     本次计算出的梯度(不考虑历史梯度).
        加入动量法后的 梯度更新公式:
            W新 = W旧 - 学习率 * St
        适用场景：
            损失函数表面较为平滑的情况；
            需要快速收敛的简单任务；
            存在震荡问题的优化场景；
            小规模模型训练；

    自适应学习率: AdaGrad(Adaptive Gradient Estimation)
        公式:
            累计平方梯度:
                St = St-1 + Gt * Gt
                解释:
                    St:     累计平方梯度
                    St-1:   历史累计平方梯度.
                    Gt:     本次的梯度.
            学习率:
                学习率 = 学习率 / (sqrt(St) + 小常数)
                解释:
                    小常数: 1e-10, 目的: 防止分母变为0
            梯度下降公式:
                W新 = W旧 - 调整后的学习率 * Gt
        缺点:
            可能会导致学习率过早, 过量的降低, 导致模型后期学习率太小, 较难找到最优解.
        适用场景：稀疏数据
                文本数据：词汇矩阵中，每篇文档只包含少量词汇；大部分词汇-文档组合都是0
                推荐系统：用户-物品评分矩阵；每个用户只会评价很少的物品
                图像处理；二值化图像中的边缘检测结果；大部分像素为0，只有边缘像素有值

    自适应学习率: RMSProp(Root Mean Square Propagation) -> 可以看做是 对AdaGrad做的优化, 加入 调和权重系数.
        公式:
            指数加权平均 累计历史平方梯度:
                St = β * St-1 +  (1 - β) * Gt * Gt
                解释:
                    St:     累计平方梯度
                    St-1:   历史累计平方梯度.
                    Gt:     本次的梯度.
                    β:      调和权重系数.
            学习率:
                学习率 = 学习率 / (sqrt(St) + 小常数)
                解释:
                    小常数: 1e-10, 目的: 防止分母变为0
            梯度下降公式:
                W新 = W旧 - 调整后的学习率 * Gt
        优点:
           RMSProp通过引入 衰减系数β, 控制历史梯度 对 历史梯度信息获取的多少.
        适用场景：
            稀疏数据处理：文本数据、推荐系统等
            非平稳目标：需要动态调整学习率的任务
            RNN训练：处理梯度消失问题

    自适应矩估计: Adam(Adaptive Moment Estimation)
        思路:
            即优化学习率, 又优化梯度.
        公式:
            一阶矩: 算均值.
                Mt = β1 * Mt-1 + (1 - β1) * Gt          充当: 梯度
                St = β2 * St-1 + (1 - β2) * Gt * Gt     充当: 学习率
            二阶矩: 梯度的方差.
                Mt^ = Mt / (1 - β1 ^ t)
                St^ = St / (1 - β2 ^ t)
            权重更新公式:
                W新 = W旧 - 学习率 / (sqrt(St^) + 小常数)  *  Mt^
        大白话翻译:
            Adam = RMSProp + Momentum
        适用场景：
            复杂深度学习模型：大型神经网络训练
            大数据集：需要高效收敛的场景
            通用首选：大多数深度学习任务的默认选择
            稀疏梯度：处理不均匀的梯度更新

总结: 如何选择梯度下降优化方法
    简单任务和较小的模型:
        SGD, 动量法
    复杂任务或者有大量数据:
        Adam
    需要处理稀疏数据或者文本数据:
        AdaGrad, RMSProp
"""

import torch
import torch.nn as nn
import torch.optim as opt

# 动量法Momentum
def momentum():
    # 初始化权重系数
    w = torch.tensor([1.0],requires_grad=True,dtype=torch.float)
    # 显式定义损失函数
    def criterion(w):
        return ((w ** 2) / 2.0).mean()
    # ⭐ 创建优化器 (普通SGD随机小批量传入参数momentum就成了动量法) 传入w需要为可迭代对象
    optimizer = opt.SGD(params=[w],lr=0.01,momentum=0.9)
    # 循环迭代更新参数
    for i in range(10):
        # 计算损失函数
        loss = criterion(w)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'动量法优化的权重w：{w.data}')

#自适应学习率Adagrad
def adagrad():
    # 初始化权重系数
    w = torch.tensor([1.0],requires_grad=True,dtype=torch.float)
    # 显式定义损失函数
    def criterion(w):
        return ((w ** 2) / 2.0).mean()
    # ⭐创建优化器
    optimizer = opt.Adagrad([w],lr=0.01)
    # 循环迭代更新参数
    for i in range(10):
        # 计算损失函数
        loss = criterion(w)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'Adagrad优化的权重w：{w.data}')

#自适应学习率PMSprop
def rmsprop():
    # 初始化权重系数
    w = torch.tensor([1.0],requires_grad=True,dtype=torch.float)
    # 显式定义损失函数
    def criterion(w):
        return ((w ** 2) / 2.0).mean()
    # ⭐创建优化器 alpha类似动量法的β，根据历史数据的调节权重系数
    optimizer = opt.RMSprop([w],lr=0.01,alpha=0.99)
    # 循环迭代更新参数
    for i in range(10):
        # 计算损失函数
        loss = criterion(w)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'RMSProp优化的权重w：{w.data}')

# 自适应矩估计Adam
def adam():
    # 初始化权重系数
    w = torch.tensor([1.0],requires_grad=True,dtype=torch.float)
    # 显式定义损失函数
    def criterion(w):
        return ((w ** 2) / 2.0).mean()
    # ⭐创建优化器 # betas=(梯度用的 衰减系数, 学习率用的 衰减系数)
    optimizer = opt.Adam([w],lr=0.01,betas=(0.9, 0.999))
    # 循环迭代更新参数
    for i in range(10):
        # 计算损失函数
        loss = criterion(w)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'Adam优化的权重w：{w.data}')


if __name__ == '__main__':
    momentum()
    adagrad()
    rmsprop()
    adam()