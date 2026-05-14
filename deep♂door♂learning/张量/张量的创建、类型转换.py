"""
张量的基本创建方式

张量：
    存储同一类型元素的容器，且元素值必须是数值
    是深度学习框架【ANN（人工神经网络）、CNN（卷积神经网络）、RNN（循环神经网络）】底层处理数据的数据结构
    张量根据维度数可以分为:
        0维张量(标量)：单个数字
        1维张量(向量)：一维数组
        2维张量(矩阵)：二维数组
        3维及以上张量：高维数组
    特点：
        张量可以运行在GPU上进行加速计算
        张量支持自动求导，这对于训练神经网络至关重要
        张量运算针对深度学习进行了优化
    张量在深度学习中的作用:
        数据表示：
        图像：通常表示为4维张量 [批次大小, 通道数, 高度, 宽度]
        文本：通常表示为2维或3维张量
        音频：通常表示为2维或3维张量
        模型参数：
        神经网络的权重和偏置都存储在张量中
        计算图：
        张量支持自动微分，这对于反向传播算法至关重要
    张量属性:
        每个张量都有以下重要属性：
        dtype：数据类型 (如 torch.float32, torch.int64)
        device：所在的设备 (CPU 或 GPU)
        shape：张量的形状
        requires_grad：是否需要计算梯度
    张量的基本创建方式：
        torch.tensor 根据指定数据创建张量（把数据转化为张量结构） ⭐
        torch.Tensor 创建指定形状的张量，也可以转换指定数据
        torch.IntTensor、torch.FloatTensor、torch.DoubleTensor 创建指定数值类型的张量
        torch.arange() torch.linspace() 创建线性张量 ⭐
        torch.random.initial_seed() torch.random.manual_seed() 设置随机种子 ⭐
        torch.rand/randn() 创建随机浮点型张量
        torch.randint(low,high,size=()) 创建随机整数型张量 ⭐
        torch.ones() torch.ones_like ⭐
        torch.zeros() torch.zeros_like
        torch.full() torch.full_like
    张量的类型转换：
        type()⭐、half()、double()、float()、short()、int()、long() 后面几个用着麻烦
        

"""
import torch
import numpy as np
# 设置随机种子
print(torch.random.initial_seed()) #返回当前随机种子值。
torch.manual_seed(42) # 设置随机种子，使随机数生成可复现。
print(torch.random.initial_seed())
print('-'*20)



def tensor(): # tensor不支持直接创建指定维度的张量
    #1. 张量标量
    t1 = torch.tensor(10)
    print(f't1:{t1},type:{type(t1)}')
    print('-'*20)

    #2. 二维列表转为二维张量
    data = [[1,1,4,5],[1,9,1,9]]
    t2 = torch.tensor(data)
    print(f't1:{t2},type:{type(t2)}')
    print('-'*20)

    #3. 二维ndarray数组转为张量
    data = np.random.randint(1,5,size=(2,8))
    t3 = torch.tensor(data)
    print(f't1:{t3},type:{type(t3)}')
    print('-'*20)

    #4. 转换张量的同时指定数值类型
    data = [[1,1,4],[5,1,4]]
    t4 = torch.tensor(data,dtype=torch.float32)
    print(f't1:{t4},type:{type(t4)}')
    print('-'*20)

def Tensor():
    """
    torch.Tensor是torch.FloatTensor的别名，是默认的张量类型  它会创建一个浮点型张量，即使输入的是整数
    Torch创建的是一个未初始化张量：在创建时没有赋予具体数值，其内部值是随机或默认的，需要后续手动赋值或通过计算填充。
    """
    #1. 创建一个一维张量
    t1 = torch.Tensor(10)
    print(f't1:{t1},type:{type(t1)}')
    print('-'*20)

    #2. 二维列表转为二维张量
    data = [[1,1,4,5],[1,9,1,9]]
    t2 = torch.Tensor(data)
    print(f't1:{t2},type:{type(t2)}')
    print('-'*20)

    #3. 二维ndarray数组转为张量
    data = np.random.randint(1,5,size=(2,8))
    t3 = torch.Tensor(data)
    print(f't1:{t3},type:{type(t3)}')
    print('-'*20)

    #4. 使用Tensor创建指定维度的张量
    t4 = torch.Tensor(2,8)
    print(f't1:{t4},type:{type(t4)}')
    print('-'*20)

def xxTensor():
    # 1. 创建一个10元素的Int类型一维张量，所有元素未初始化
    t1 = torch.IntTensor(10)
    print(f't1:{t1},type:{type(t1)},\n dtype:{t1.dtype}')
    print('-' * 20)

    # 2. 将二维列表转换为Float类型张量
    data = [[1, 1, 4, 5], [1, 9, 1, 9]]
    t2 = torch.FloatTensor(data)
    print(f't2:{t2},type:{type(t2)},\n dtype:{t2.dtype}')
    print('-' * 20)

    # 3. 将二维ndarray数组转换为Double类型张量
    data = np.random.randint(1, 5, size=(2, 8))
    t3 = torch.DoubleTensor(data)
    print(f't3:{t3},type:{type(t3)},\n dtype:{t3.dtype}')
    print('-' * 20)

    # 4. 创建2×8的Int类型二维张量，所有元素未初始化
    t4 = torch.IntTensor(2, 8)
    print(f't4:{t4},type:{type(t4)},\n dtype:{t4.dtype}')
    print('-' * 20)

def linear():
    #1. 创建指定范围的线性张量 第三个参数为步长
    t5 = torch.arange(1,5,0.1) # 如果起始结束和步长都是整数的话创建的张量也是整数类型
    print(f't5:{t5},type:{type(t5)},\n dtype:{t5.dtype}')
    print('-' * 20)

    #2. 创建等差数列张量 第三个参数为个数
    t6 = torch.linspace(1,5,9)
    print(f't6:{t6},type:{type(t6)},\n dtype:{t6.dtype}')
    print('-' * 20)

def rand():
    #1. 创建均匀分布的随机张量
    t7 = torch.rand(size=(7,7))
    print(f't7:{t7},type:{type(t7)},\n dtype:{t7.dtype}')
    print('-' * 20)

    #2. 创建正态分布的随机张量
    t8 = torch.randn(size=(7,7))
    print(f't8:{t8},type:{type(t8)},\n dtype:{t8.dtype}')
    print('-' * 20)
    
    #3. 自定正态分布的均值和方差
    t9 = torch.normal(114, 514, size=(5, 3))
    print(f't9:{t9},type:{type(t9)},\n dtype:{t9.dtype}')
    print('-' * 20)

    #4. 生成随机整数张量
    t10 = torch.randint(1,5,size=(2,8))
    print(f't10:{t10},type:{type(t10)},\n dtype:{t10.dtype}')
    print('-' * 20)

def ones():
    #1. 创建全一张量
    t11 = torch.ones(size=(1,5),dtype=torch.int)
    print(f't11:{t11},type:{type(t11)},\n dtype:{t11.dtype}')
    print('-' * 20)

    #2. 基于指定张量形状创建全一张量 只能传入张量
    _ = np.array([[114,514,1919,810],[114,115,116,119]],dtype=np.float_)
    data = torch.tensor(_,dtype=torch.int)
    t12 = torch.ones_like(data)
    print(f't12:{t12},type:{type(t12)},\n dtype:{t12.dtype}')
    print('-' * 20)

def zeros():
    #1. 创建全零张量
    t13 = torch.zeros(size=(1,5),dtype=torch.int)
    print(f't13:{t13},type:{type(t13)},\n dtype:{t13.dtype}')
    print('-' * 20)

    #2. 基于指定张量形状创建全零张量
    _ = np.array([[114,514,1919,810],[114,115,116,119]],dtype=np.float_)
    data = torch.tensor(_,dtype=torch.int)
    t14 = torch.zeros_like(data)
    print(f't14:{t14},type:{type(t14)},\n dtype:{t14.dtype}')
    print('-' * 20)

def full():
    #1. 创建全张量
    t15 = torch.full(size=(1,5),fill_value=255,dtype=torch.int)
    print(f't15:{t15},type:{type(t15)},\n dtype:{t15.dtype}')
    print('-' * 20)

    #2. 基于指定张量形状创建全张量
    _ = np.array([[114,514,1919,810],[114,115,116,119]],dtype=np.float_)
    data = torch.tensor(_,dtype=torch.int)
    t16 = torch.full_like(data,fill_value=255)
    print()

def type_conversion():
    t16 = torch.tensor([[114,514,1919,810],[114,115,116,119]],dtype=torch.float32)
    print(f't16:{t16},元素类型：{t16.dtype},数据类型（张量）：{type(t16)}')
    
    #1. 创建张量后使用type()进行类型转换
    t17 = t16.type(torch.int)
    print(f't17:{t17},元素类型：{t17.dtype},数据类型（张量）：{type(t17)}')

    #2. 创建张量后使用half()、double()、float()、short()、int()、long()进行类型转换
    print(t16.half().dtype)
    print(t16.float().dtypge)
    print(t16.double().dtype)
    print(t16.short().dtype)
    print(t16.int().dtype)
    print(t16.long().dtype)



if __name__ == '__main__':
    # tensor()
    # Tensor()
    xxTensor()
    # linear()
    # rand()
    # ones()
    # zeros()
    # full()
    # type_conversion()






