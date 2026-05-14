"""
演示自动微分模块
步骤：
    1. 定义 权重、偏置 张量
    2. 定义损失蛤属
    3. 利用梯度下降法 循环迭代100次 更新权重：
        3.1 正向计算预测值(前向传播)
        3.2 梯度清零 w.grad.zero_()
        3.3 反向传播
        3.4 梯度更新 w.data = w.data - 0.01 * w.grad
细节:
    只有标量张量才能求导, 且大多数底层操作的都是 浮点型, 记得转型.
"""

import torch

# 入门演示自动微分之单步权重更新
def demo1():
    # 1. 定义权重张量
    w = torch.randn(size=(3, 3), requires_grad=True)
    print(f'权重张量: {w}')
    print('——' * 20)
    # 2. 定义损失函数
    loss_func = 2 * w ** 2

    # 3. 查看梯度函数类型（了解·）
    # print(f'梯度函数类型: {type(loss_func.grad_fn)}') # 梯度函数类型: <class 'MulBackward0'>
    print(loss_func.sum())
    print('——' * 20)
    # 4. 计算梯度，记录到w.grad 属性中
    loss_func.mean().backward()  # 使用mean()保证loss值是一个标量，标量张量才能求导

    # 5. 带入权重更新公式，计算新的权重
    w_new = w.data - 0.1 * w.grad

    # 6. 打印更新后结果
    print(f'更新后的权重: {w_new}')
    print('——' * 20)
    print(f'单词调整幅度：\n{w.data - w_new}')

# 演示手动迭代更新（实际不需要，有专门的优化器）
def demo2():
    # 1. 定义权重及偏置张量
    w = torch.tensor(9.0, requires_grad=True)
    b = torch.tensor(2.0, requires_grad=True)
    print(f'初始权重张量: {w}')
    print(f'初始偏置张量: {b}')
    print('——' * 20)

    # 3. 梯度下降循环迭代
    for i in range(20):  # 减少迭代次数以便观察
        # 3.1 前向传播 - 复用计算图
        loss = w ** 2 + b

        # 3.2 梯度清零 不知道为什么我的梯度不会累积，不过实际开发中需要清零
        if w.grad is not None:
            w.grad.zero_()
        if b.grad is not None:
            b.grad.zero_()

        # 3.3 反向传播
        loss.backward()

        # 3.4 参数更新
        with torch.no_grad():
            """
在PyTorch中，默认情况下所有涉及requires_grad=True的张量的操作都会被跟踪，以构建计算图。但在某些情况下，我们不希望这种跟踪发生：
    参数更新时 - 我们只是想修改参数值，而不是构建计算图
    模型推理时 - 我们只关心结果，不关心梯度
    评估模型时 - 不需要计算梯度来节省内存和时间
            """
            w.data = w.data - 0.1 * w.grad
            b.data = b.data - 0.1 * b.grad

        print(f'第{i+1}次迭代，损失: {loss.item()}')
        print(f'第{i+1}次迭代，权重: {w.item()}')
        print(f'第{i+1}次迭代，偏置: {b.item()}')
        print('——'*20)

def detach_demo():
    #    演示一下detach的作用
    #    简述：tensor张量设置自动微分后无法转为ndarray数组，需要先通过detach转换
    t1 = torch.tensor([1, 2, 3], requires_grad=True,dtype=torch.float)
    print(f't1: {t1},dtype: {t1.dtype}')

    # n1 = t1.numpy()    #报错
    # print(f'n1: {n1},dtype: {n1.dtype}')

    n1 = t1.detach().numpy()
    print(f'n1: {n1},dtype: {n1.dtype}')
    print('——'*20)

    # 演示共享内存
    t1.data[0] = 4
    print(f't1: {t1}')
    print(f'n1: {n1}')

if __name__ == '__main__':
    # demo1()
    # demo2()
    detach_demo()