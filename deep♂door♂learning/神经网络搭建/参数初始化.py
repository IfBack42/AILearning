"""
演示参数初始化的7钟方式

参数初始化目的：
    1.防止梯度消失或梯度爆炸
    2.提高收敛效率
    3.打破对称性

参数初始化方式：
    1.全0、全1、固定值初始化  无法打破对成性
    2.随机初始化、正态分布初始化、kaiming初始化、xavier初始化    可以打破对称性

总结：
    1.主要使用kaiming、Xavier、全0初始化
    2.ReLU系列：优先kaiming
    3.非ReLU：优先xavier
    4.浅层网络：可以考虑 随机初始化
"""

import torch.nn as nn
import torch

# 均匀随机分布初始化 0-1 均匀参数
def uniform():
    # 1.创建线性层
    linear1 = nn.Linear(5,3)
    # 2.权重初始化
    nn.init.uniform_(linear1.weight) # _ 表示替换源数据，inplace
    # 3.偏置初始化
    nn.init.uniform_(linear1.bias)
    # 4.打印结果
    print(linear1.weight.data)
    print(linear1.bias.data)

# 固定值初始化
def constant():
    # 1.创建线性层
    linear2 = nn.Linear(5,3)
    # 2.权重初始化
    nn.init.constant_(linear2.weight,3)
    # 3.偏置初始化
    nn.init.constant_(linear2.bias,0)
    # 4.打印结果
    print(linear2.weight.data)
    print(linear2.bias.data)

# 全零初始化
def zeros():
    # 1.创建线性层
    linear3 = nn.Linear(5,3)
    # 3.权重初始化
    nn.init.zeros_(linear3.weight)
    # 3.偏置初始化
    nn.init.zeros_(linear3.bias)
    # 4.打印结果
    print(linear3.weight.data)
    print(linear3.bias.data)

# 全1初始化
def ones():
    # 1.创建线性层
    linear4 = nn.Linear(5,3)
    # 2.权重初始化
    nn.init.ones_(linear4.weight)
    # 3.偏置初始化
    nn.init.ones_(linear4.bias)
    # 4.打印结果
    print(linear4.weight.data)
    print(linear4.bias.data)

# 正态分布随机初始化
def normal():
    # 1.创建线性层
    linear5 = nn.Linear(5,3)
    # 2.权重初始化
    nn.init.normal_(linear5.weight)
    # 3.偏置初始化
    nn.init.normal_(linear5.bias)
    # 4.打印结果
    print(linear5.weight.data)
    print(linear5.bias.data)

# kaiming初始化 不能用来初始化偏置，而且不能这样用
def kaiming():
    # 1.kaiming正态分布初始化
    linear6 = nn.Linear(5,3)
    nn.init.kaiming_normal_(linear6.weight)
    # 2.kaiming均匀分布初始化
    # nn.init.kaiming_uniform_(linear6.weight)
    print(linear6.weight.data)
    print(linear6.bias.data)

# xavier初始化
def xavier():
    # 1.xavier正态分布初始化
    linear7 = nn.Linear(5,3)
    nn.init.xavier_normal_(linear7.weight)
    # 2.xavier均匀分布初始化
    # nn.init.xavier_uniform_(linear7.weight)
    print(linear7.weight.data)
    print(linear7.bias.data)



if __name__ == '__main__':
    # uniform()
    # constant()
    # zeros()
    # ones()
    # normal()
    kaiming()
    xavier()