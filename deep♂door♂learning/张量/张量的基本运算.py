"""
张量的基本运算操作：

    +,-,*,/ 符号任然通用，
    张量和数值的运算：该数值会与张量中的所有元素进行相应运算
    add(),sub(),mul(),div(),neg()          加减乘除，取反
    add()_,sub()_,mul()_,div()_,neg()_     加上_可以修改源数据，类似inplace=True

张量的点乘和矩阵乘法：
    点乘：*，mul()，要求两个张量形状一致，直接进行对应元素相乘
    叉乘：matmul(),@要求前一个张量的列数等于后一个张量的行数
    dot：对一维张量有效，对应元素相乘再相加，得到标量张量

张量的常用运算函数：
    sum(),max(),min(),mean()                都有dim参数，0表示列，1表示行 很烦
    pow(),sqrt(),exp(),log():e为底,log2(),log10()     没有dim参数

"""

import torch
torch.manual_seed(42)
def operations1():
    t1 = torch.randint(1,10,(2,3))
    print(f't1: {t1}')

    # 演示加法，其余效果相似
    t2 = t1 + 10
    t2 = t1.add(10)
    t2 = t1.add_(10)
    print(f't2: {t2}')
    print(f't1: {t1}')

def mul():
    # 演示张量点乘
    t1 = torch.randint(1,10,(3,2))
    t2 = torch.randint(1,10,(3,2))
    print(t1,t2,sep="\n")
    t3 = t1 * t2
    t3 = t1.mul(t2)
    print(t3)

    # 演示张量叉乘
    t4 = torch.randint(1,10,(2,8))
    t5 = t1 @ t4
    t5 = t1.matmul(t4)
    print(t5)

    # 演示dot
    t6 = torch.tensor([1,1,4])
    t7 = torch.tensor([5,1,4])
    print(t6.dot(t7))

def operations2():
    t1 = torch.tensor([[1,1,4],[5,1,4]],dtype=torch.float)
    print(f't1: {t1}')
    print('——'*20)

    # 演示有dim参数的函数
    print(f'ti.sum(dim=0):{t1.sum(dim=0)}')
    print(f'ti.sum(dim=1):{t1.sum(dim=1)}')
    print(f'ti.sum():{t1.sum()}')
    print('——'*20)
    #max,min
    print(f't1.max(dim=0):{t1.max(dim=0)}')
    print(f't1.max(dim=0):{t1.max(dim=1)}')
    print(f't1.max():{t1.max()}')
    print('——'*20)
    #mean
    print(f't1.mean(dim=0):{t1.mean(dim=0)}')
    print(f't1.mean(dim=1):{t1.mean(dim=1)}')
    print(f't1.mean():{t1.mean()}')
    print('——'*20)

    # 演示不含dim的函数
    print(f't1.pow(2):{t1.pow(2)}')
    print(f't1.sqrt():{t1.sqrt()}')
    print(f't1.exp(n):{t1.exp()}')
    print(f't1.log():{t1.log()}')   # 啥也不传
    print(f't1.log2():{t1.log2()}')
    print(f't1.log10():{t1.log10()}')



if __name__ == '__main__':
    # operations1()
    # mul()
    operations2()