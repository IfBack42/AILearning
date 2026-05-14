"""
演示张量的形状变换操作：
    reshape():          不改变张量内容前提下，对张量的形状进行改变。
    unsqueeze():        在指定的轴上增加一个维度，等价于：升维。
    squeeze():          删除所有为1的维度，等价于：降维。
    transpose():        一次只能交换两个维度。
    permute():          一次可以同时交换多个维度。
    view():             改变张量的形状，但不改变张量的内容。
    contiguous():       改变张量的形状，并改变张量的内容。
    is_contiguous():    判断张量的内容是否连续。
"""

import torch
torch.manual_seed(42)

def basic_reshape():
    # 演示最基本的reshape操作：reshape转换前后张量元素个数必须一致
    t1 = torch.randint(low=1,high=10,size=(2,6))
    print(f't1: {t1},\n shape: {t1.shape}')
    print('——' * 20)

    t2 = t1.reshape(shape=(1,12))
    print(f't2: {t2},\n shape: {t2.shape}')
    print('——' * 20)

def squeeze_unsqueeze():
    # 演示squeeze_unsqueeze的升维降维操作：无法跨越维度创建新维度
    t1 = torch.randint(1,10,(2,3,2,1))
    print(f't1: {t1},\n shape: {t1.shape}')
    print('——' * 20)

    # 在0维增加一个维度
    t2 = t1.unsqueeze(0)
    print(f't2: {t2},\n shape: {t2.shape}')
    print('——' * 20)

    # 在1维增加一个维度
    t3 = t1.unsqueeze(1)
    print(f't3: {t3},\n shape: {t3.shape}')
    print('——' * 20)

    # 删除所有元素为1的维度
    t4 = t1.squeeze()
    print(f't4: {t4},\n shape: {t4.shape}')
    print('——' * 20)

def advanced_reshape():
    # 演示transpose和permute，交换张量维度
    t1 = torch.randint(1,10,(4,2,3))
    print(f't1: {t1},\n shape: {t1.shape}')
    print('——' * 20)

    # transpose()
    t2 = t1.transpose(0,2)   # 交换俩维度
    print(f't2: {t2},\n shape: {t2.shape}')
    print('——' * 20)

    # permute
    t3 = t1.permute(2,0,1)  # 任意排序交换维度
    print(f't3: {t3},\n shape: {t3.shape}')
    print('——' * 20)

    # view
    t4 = t1.view(12,2)  # 转换为任意形状任意维度
    print(f't4: {t4},\n shape: {t4.shape}')
    print('——' * 20)

def conti():
    # 演示contiguous 判断张量是否连续
    t1 = torch.randint(1,10,(2,3,4))
    print(f't1: {t1},\n shape: {t1.shape}')
    print('——' * 20)

    # is_contiguous 判断张量中数据顺序是否和内存存储顺序一致
    print(f't1 is_contiguous: {t1.is_contiguous()}')
    print('——' * 20)

    # 使用view修改张量形状后判断是否连续
    # view无法改变不连续的张量的形状，比如使用transpose改变结果的张量
    t2 = t1.view(6,4)
    print(f't2 is_contiguous: {t2.is_contiguous()}')
    print('——' * 20)

    # 使用transpose修改张量形状后判断是否连续
    t3 = t1.transpose(0,2)
    print(f't3 is_contiguous: {t3.is_contiguous()}')
    print('——' * 20)

    # 使用contiguous将不连续张量转为连续张量后判断是否连续
    t4 = t3.contiguous()
    print(f't4 is_contiguous: {t4.is_contiguous()}')
    print('——' * 20)



if __name__ == '__main__':
    # basic()
    # squeeze_unsqueeze()
    advanced_reshape()
    # conti()