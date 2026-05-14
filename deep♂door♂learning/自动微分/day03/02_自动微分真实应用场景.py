"""
案例:
    演示自动微分的真实应用场景.

结论:
    1. 先前向转播(正向传播) 计算出 预测值(z)
    2. 基于损失函数, 结合 预测值(z) 和 真实值(y), 来计算 梯度.
    3. 结合权重更新公式 w新 = w旧 - 学习率 * 梯度, 来更新 权重.
"""

# 导包
import torch

# 1. 定义x, 表示: 特征(输入数据), 假设: 2行5列, 全1矩阵.
x = torch.ones(2, 5)
print(f'x: {x}')

# 2. 定义y, 表示: 标签(真实值), 假设: 2行3列, 全0矩阵.
y = torch.zeros(2, 3)
print(f'y: {y}')

# 3. 初始化(可自动微分的)权重 和 偏置.
w = torch.randn(5, 3, requires_grad=True)
print(f'w: {w}')

b = torch.randn(3, requires_grad=True)
print(f'b: {b}')

# 4. 前向转播(正向传播), 计算出 预测值(z).
z = torch.matmul(x, w) + b
# z = x @ w + b
print(f'z: {z}')

# 5. 定义损失函数.
criterion = torch.nn.MSELoss()  # neural network: 神经网络
loss = criterion(z, y)          # loss = 损失
print(f'loss: {loss}')

# 6. 进行自动微分, 求导, 结合反向传播, 更新权重.
loss.backward()

# 7. 打印w, b 用来更新的梯度.
print(f'w的梯度: {w.grad}')
print(f'b的梯度: {b.grad}')

# 后续就是: w新 = w旧 - 学习率 * 梯度, 来更新 权重.