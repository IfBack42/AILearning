"""
张量的拼接方式：
    cat()       不会改变轴数，除了拼接的维度外，其他维度必须保持一致
    stack()     改变轴数，所有维度必须保持一致
"""

import torch
torch.manual_seed(42)

t1 = torch.randint(0, 10, (2, 3))
print(f't1: {t1},\nshape: {t1.shape}')
print('——' * 20)

t2 = torch.randint(0, 10, (2, 3))
print(f't2: {t2},\nshape: {t2.shape}')
print('——' * 20)

# 演示cat拼接
t3 = torch.cat([t1,t2],dim=0)
print(f't3: {t3},\nshape: {t3.shape}')

t4 = torch.cat([t1,t2],dim=1)
print(f't4: {t4},\nshape: {t4.shape}')
print('——' * 20)

# 演示stack拼接，所有轴必须一致，可以生成新维度不能跨越
t5 = torch.stack([t1,t2],dim=1)
print(f't5: {t5},\nshape: {t5.shape}')
print('——' * 20)

t6 = torch.stack([t1,t2],dim=2)
print(f't6: {t6},\nshape: {t6.shape}')
print('——' * 20)

