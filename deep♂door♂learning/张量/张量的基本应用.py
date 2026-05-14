"""
演示张量和numpy的相互转换以及从标量张量中提取内容

涉及到的API：
    张量 转 numpy：
        张量对象.numpy()                                     共享内存
        张量对象.numpy.copy()     不共享内存⭐
    numpy ndarray 转 张量：
        from_numpy()                                        共享内存
        torch.tensor                                        不共享内存
    从标量张量中提取内容：
        标量张量.item()
"""

import torch
import numpy as np

def t2n():
    t1 = torch.tensor([[114,514],[1919,810]])
    print(f't1:{t1},元素类型：{t1.dtype},数据类型（张量）：{type(t1)}')
    print('-'*50)
    n1 = t1.numpy() # 共享内存
    n2 = t1.numpy().copy() # 不共享内存
    print('-'*50)
    n1[0][0] = 114514
    print(f't1:{t1}')
    print(f'n1:{n1}')
    print(f'n2:{n2}')

def n2t():
    n1 = np.array([[114,514],[1919,810]])
    print(f'n1:{n1},元素类型：{n1.dtype},数据类型（numpy）：{type(n1)}')
    t1 = torch.from_numpy(n1) # 共享内存
    print(f't1:{t1},元素类型：{t1.dtype},数据类型（张量）：{type(t1)}')
    t2 = torch.tensor(n1) # 不共享内存
    print(f't2:{t2},元素类型：{t2.dtype},数据类型（张量）：{type(t2)}')
    print('-'*50)
    n1[0][0] = 2
    print(f'n1:{n1}')
    print(f't1:{t1}')
    print(f't2:{t2}')

def extract():
    t1 = torch.tensor(6.6)
    # t1 = torch.tensor([[114,514],[1919,810]]) # item只能提取标量
    print(f't1:{t1},tycpe:{type(t1)}')
    value = t1.item()
    print(f'value:{value},type:{type(value)}')



if __name__ == '__main__':
    # t2n()
    # n2t()
    extract()