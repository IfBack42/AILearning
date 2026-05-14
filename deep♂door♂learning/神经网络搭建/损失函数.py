"""
损失函数演示

损失函数选择：
    分类问题:
        多分类交叉熵损失: CrossEntropyLoss
        二分类交叉熵损失: BCELoss
    回归问题:
        MAE: Mean Absolute Error, 平均绝对误差.
        MSE: Mean Squared Error, 均方误差.
        Smooth L1: 结合上述两个的特点做的升级, 优化.

1.多分类交叉熵损失: CrossEntropyLoss
    设计思路:
        Loss = - Σy log(S(f(x)))
    简单记忆:
        x:          样本
        f(x):       加权求和
        S(f(x)):    处理后的概率
        y:          样本x属于某一个类别的 真实概率.
    细节:CrossEntropyLoss = Softmax() + 损失计算, 后续如果用这个损失函数, 则: 输出层就不用额外调用 softmax()激活函数了.

2.二分类任务损失:BCEloss(Sigmoid)
    公式:
        Loss = -ylog(预测值) - (1 - y)log(1 - 预测值)
    细节:
        因为公式中没有包含Sigmoid激活函数, 所以使用BCELoss的时候, 还需要手动指定 Sigmoid.

3.回归任务的损失函数：

    3.1 MAE(L1loss):   Mean Absolute Error, 平均绝对误差.
        公式:
            误差绝对值之和 / 样本总数
        类似于L1正则化, 权重可以降维0, 数据会变得稀疏.

        弊端:
            在0点不平滑, 可能错过最小值.

    3.2 MSE:   Mean Squared Error, 均方误差.
        公式:
            误差平方之和 / 样本总数
        弊端:
            如果差值过大, 可能存在梯度爆炸的情况.

    3.3 Smooth L1:
        就是基于MAE 和 MSE做的综合, 在 [-1, 1]是 L2(MSE), 其它段时L1.
        这样即解决了L1不平滑的问题(0点不可导, 可能错过最小值)
        又解决了L2(MSE)的 梯度爆炸的问题.
"""

import torch
import torch.nn as nn

def cross_entropy_loss():
    # 1.创建真实值数据
    y_true = torch.tensor([[0,1,0],[1,0,0]],dtype=torch.float)
    # 2.创建预测值数据
    y_pred = torch.tensor([[0.1,0.8,0.1],[0.7,0.2,0.1]],dtype=torch.float,requires_grad=True)
    # 3.创建损失函数
    criterion = nn.CrossEntropyLoss() # 输出值为特征列平均损失
    # 4.计算损失
    loss = criterion(y_pred,y_true)
    print(f'多分类交叉熵损失：{loss}')

def bce_loss():
    # 1.创建真实值数据
    y_true = torch.tensor([0,1,0],dtype=torch.float)
    # 2.创建预测值数据(概率)
    y_pred = torch.tensor([0.6901,0.5423,0.2639],dtype=torch.float,requires_grad=True)
    # 3.创建损失函数
    criterion = nn.BCELoss() # 输出值为特征列平均损失
    # 4.计算损失
    loss = criterion(y_pred,y_true)
    print(f'二分类损失：{loss}')

def mae():
    # 1.创建真实值数据
    y_true = torch.tensor([2.0,2.0,2.0],dtype=torch.float)
    # 2.创建预测值数据(概率)
    y_pred = torch.tensor([1.0,1.0,1.9],dtype=torch.float,requires_grad=True)
    # 3.创建损失函数
    criterion = nn.L1Loss()
    # 4.计算损失
    loss = criterion(y_pred,y_true)
    print(f'MAE损失：{loss}')

def mse():
    # 1.创建真实值数据
    y_true = torch.tensor([2.0,2.0,2.0],dtype=torch.float)
    # 2.创建预测值数据(概率)
    y_pred = torch.tensor([1.0,1.0,1.9],dtype=torch.float,requires_grad=True)
    # 3.创建损失函数
    criterion = nn.MSELoss()
    # 4.计算损失
    loss = criterion(y_pred,y_true)
    print(f'MSE损失：{loss}')

def smoothl1():
    # 1.创建真实值数据
    y_true = torch.tensor([2.0,2.0,2.0],dtype=torch.float)
    # 2.创建预测值数据(概率)
    y_pred = torch.tensor([1.0,1.0,1.9],dtype=torch.float,requires_grad=True)
    # 3.创建损失函数
    criterion = nn.SmoothL1Loss()
    # 4.计算损失
    loss = criterion(y_pred,y_true)
    print(f'SmoothL1损失：{loss}')


if __name__ == '__main__':
    cross_entropy_loss()
    bce_loss()
    mae()
    mse()
    smoothl1()