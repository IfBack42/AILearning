"""
演示学习率衰减策略.

学习率衰减策略介绍:
    目的:
        较之于AdaGrad, RMSProp, Adam方式, 我们可以通过 等间隔, 指定间隔, 指数等方式, 来手动控制学习率的调整.

    分类:
        等间隔学习率衰减
        指定间隔学习率衰减
        指数学习率衰减

等间隔学习率衰减:
    step_size: 间隔的轮数, 即: 多少轮调整一次学习率.
    gamma:     学习率衰减系数, 即: lr新 = lr旧 * gamma

指定间隔学习率衰减:
    milestones = [50, 125, 160]     里边定义的是要调整学习率的 轮数.
    gamma:     学习率衰减系数, 即: lr新 = lr旧 * gamma

指数间隔学习率衰减:
    前期学习率衰减快, 中期慢, 后期更慢, 更符合梯度下降规律.
    公式:
        lr新 = lr旧 * gamma ** epoch

总结:
    等间隔学习率衰减:
        优点:
            直观, 易于调试, 适用于 大批量数据.
        缺点:
            学习率变化较大, 可能跳过最优解.
        应用场景:
            大型数据集, 较为简单的任务,训练周期较长的项目,对学习率调整时机要求不严格的任务

    指定间学习率衰减:
        优点:
            易于调试, 稳定训练过程.
        缺点:
            在某些情况下可能衰减过快, 导致优化提前停滞.
        应用场景:
            对训练平稳性要求较高的任务,需要在特定训练阶段调整学习率的任务,已知最佳学习率调整时机的情况
   指数学习率衰减:
        优点:
            平滑, 且考虑历史更新, 收敛稳定性较强.
        缺点:
            超参调节较为复杂, 可能需要更多的资源.
        应用场景:
            高精度训练, 避免过快收敛,需要平滑学习率过渡的高精度训练,对收敛稳定性要求极高的任务

"""
import torch
import torch.nn as nn
from torch import optim as opt
import matplotlib.pyplot as plt

def equal():
    # 定义变量记录初始学习率、训练轮数、批次数
    lr, epochs, batch_size = 0.1, 200, 10

    # 创建示例数据 y_true, x, w
    y_true = torch.tensor([0])
    w = torch.tensor([1.0],requires_grad=True,dtype=torch.float)
    x = torch.tensor([1.0],dtype=torch.float)

    # 定义损失函数
    def criterion(w,x):
        return (w * x - y_true) ** 2

    # 创建动量法优化器对象
    optimizer = opt.SGD([w],lr=lr,momentum=0.9)
    # 创建等间隔学习率衰减对象
    scheduler = opt.lr_scheduler.StepLR(optimizer,step_size=50,gamma=0.5) # gamma:学习率衰减系数,更新后学习率=lr*gamma
    # 创建列表, 记录训练轮数、 每轮训练用的学习率
    lr_list, epoch_list = [], []

    # 循环迭代并记录
    for epoch in range(epochs):
        # 记录当前轮数和学习率
        epoch_list.append(epoch)
        lr_list.append(scheduler.get_last_lr())
        # 根据批次迭代
        for i in range(batch_size):
            # 参数更新4步走 + 学习率更新的1步
            loss = criterion(w,x)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # 每轮结束后自动判断并更新学习率
        scheduler.step() # 学习率优化特有
    print(f'lr_list: {lr_list}')

    # x轴: 训练的轮数, y轴: 每轮训练用的学习率
    plt.plot(epoch_list, lr_list)
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.show()

def designate():
    # 定义变量记录初始学习率、训练轮数、批次数
    lr, epochs, batch_size = 0.1, 200, 10

    # 创建示例数据 y_true, x, w
    y_true = torch.tensor([0])
    w = torch.tensor([1.0],requires_grad=True,dtype=torch.float)
    x = torch.tensor([1.0],dtype=torch.float)

    # 定义损失函数
    def criterion(w,x):
        return (w * x - y_true) ** 2

    # 创建动量法优化器对象
    optimizer = opt.SGD([w],lr=lr,momentum=0.9)
    # 创建等间隔学习率衰减对象
    # 定义变量, 记录要修改学习率的轮数.
    milestones = [50, 125, 160]
    scheduler = opt.lr_scheduler.MultiStepLR(optimizer,milestones=milestones,gamma=0.5) # gamma:学习率衰减系数,更新后学习率=lr*gamma
    # 创建列表, 记录训练轮数、 每轮训练用的学习率
    lr_list, epoch_list = [], []

    # 循环迭代并记录
    for epoch in range(epochs):
        # 记录当前轮数和学习率
        epoch_list.append(epoch)
        lr_list.append(scheduler.get_last_lr())
        # 根据批次迭代
        for i in range(batch_size):
            # 参数更新4步走 + 学习率更新的1步
            loss = criterion(w,x)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # 每轮结束后自动判断并更新学习率
        scheduler.step() # 学习率优化特有
    print(f'lr_list: {lr_list}')

    # x轴: 训练的轮数, y轴: 每轮训练用的学习率
    plt.plot(epoch_list, lr_list)
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.show()

def exp():
    # 定义变量记录初始学习率、训练轮数、批次数
    lr, epochs, batch_size = 0.1, 200, 10

    # 创建示例数据 y_true, x, w
    y_true = torch.tensor([0])
    w = torch.tensor([1.0],requires_grad=True,dtype=torch.float)
    x = torch.tensor([1.0],dtype=torch.float)

    # 定义损失函数
    def criterion(w,x):
        return (w * x - y_true) ** 2

    # 创建动量法优化器对象
    optimizer = opt.SGD([w],lr=lr,momentum=0.9)
    # 创建等间隔学习率衰减对象
    scheduler = opt.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
    # 创建列表, 记录训练轮数、 每轮训练用的学习率
    lr_list, epoch_list = [], []

    # 循环迭代并记录
    for epoch in range(epochs):
        # 记录当前轮数和学习率
        epoch_list.append(epoch)
        lr_list.append(scheduler.get_last_lr())
        # 根据批次迭代
        for i in range(batch_size):
            # 参数更新4步走 + 学习率更新的1步
            loss = criterion(w,x)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # 每轮结束后自动判断并更新学习率
        scheduler.step() # 学习率优化特有
    print(f'lr_list: {lr_list}')

    # x轴: 训练的轮数, y轴: 每轮训练用的学习率
    plt.plot(epoch_list, lr_list)
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.show()


if __name__ == '__main__':
    # equal()
    # designate()
    exp()