"""
案例：使用pytorch组件模拟线性回归

步骤：
    1.准备数据集     使用pytorch.data.DataLoader
        1.1 数据准备：将原始数据转换为张量（Tensor）格式
        1.2 数据封装：使用数据集对象（如TensorDataset）组织数据
        1.3 数据加载：使用DataLoader进行批量加载和预处理
            批次大小：训练n轮，每一轮训练 数据总量/批次大小 次
    2.构建模型       使用pytorch.nn.Linear
    3.设置损失函数    使用pytorch.nn.MSELoss
    4.创建优化器      使用pytorch.optim.SGD
    5.模型训练

注意计算图问题：
    参与计算图：模型参数、由模型参数计算得出的张量
    不参与计算图：原始数据、手动创建的张量（默认）
    需要detach()：当要将参与计算图的张量用于不需要梯度的场景时
        # 1. 模型参数（自动参与）
        model = nn.Linear(1, 1)  # weight和bias默认requires_grad=True
        # 2. 输入数据（不参与）
        x = torch.tensor(...)  # 默认requires_grad=False
        # 3. 模型预测（参与）
        y_pre = model(x)  # 因为model.weight和model.bias需要梯度，所以y_pre也参与
        # 4. 损失计算（参与）
        loss = criterion(y_pre, y_train)  # y_pre参与，所以loss也参与
        # 5. 真实值计算（不参与）
        y_true = coef * x + 11.4  # coef和x都不需要梯度，所以y_true不参与
"""

import torch
from torch import nn                # 提供构建神经网络所需的各种类和函数，包括层、激活函数、损失函数、优化器等。
from sklearn.datasets import make_regression    # 生成数据
from torch.utils.data import TensorDataset      # 构建数据集对象
from torch.utils.data import DataLoader      # 数据加载器
from torch import optim           # 优化器模块，提供不同优化算法，如SGD随机梯度下降、Adam自适应矩估计、Adagrad自适应梯度算法 等。
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

def create_dataset():
    x,y,coef = make_regression(
        n_samples=100,
        n_features=1,
        noise=10,
        coef=True,
        bias=11.4,
        random_state=42
    )
    x = torch.tensor(x,dtype=torch.float)
    y = torch.tensor(y,dtype=torch.float).reshape(-1,1)
    coef = torch.tensor(coef,dtype=torch.float)
    # print(x,y,sep='\n')
    print(f'初始权重为：{coef},初始偏置为：{11.4}')

    return x,y,coef

def model_train():
    x,y,coef = create_dataset()
    # 创建数据集对象：把数据有序打包起来，方便后续使用，提高效率
    dataset = TensorDataset(x,y)
    # 创建数据加载器对象：建立在Dataset之上，提供了批量处理、数据打乱、并行加载等功能
    #                                   👇批次大小     👇是否打乱数据
    dataloader = DataLoader(dataset,batch_size=16,shuffle=True)
    # 创建初始线性回归模型   👇输入特征   👇输出特征    神经网络模型可以有多个输出
    model = nn.Linear(in_features=1,out_features=1)
    # 创建损失函数对象
    criterion = nn.MSELoss()
    # 创建优化器对象：优化器把求导，反向传播，梯度清零，权重优化打包好了，不需要自己慢慢搞
    # 传入模型参数和学习率
    optimizer = optim.SGD(model.parameters(),lr=0.01)

    # 训练具体过程
    epochs = 300  # 训练论数
    loss_list = [] # 列表记录损失

    for epoch in range(1,epochs+1):
        # 每轮分批次训练，一批为一个batch
        total_batch_loss = 0.0 # 记录每批次损失，计算每轮损失
        n = 0 # 记录批次数
        for x_train,y_train in dataloader: # 16条/批 一轮训练 100/16 = 7 次
            # 模型预测，计算平均损失
            y_pre = model(x_train)
            loss = criterion(y_pre,y_train) # loss不是一个简单的数字，而是一个包含计算图信息的张量，所以这里使用loss来backgrid

            # 记录损失
            print(loss,type(loss))
            total_batch_loss += loss.item()
            n += 1

            # 按顺序：梯度清零、反向传播、权重更新 优化器的参数更新不需要显式使用上下文管理器防止追踪
            optimizer.zero_grad()  # 梯度清零
            loss.backward()  # 反向传播, 计算梯度
            optimizer.step()  # 梯度更新
        # 记录每轮损失
        mean_loss = total_batch_loss/n
        loss_list.append(mean_loss)
        print(f'第{epoch}轮，损失为：{mean_loss}')

    # 打印模型最终参数
    w = model.weight.item()
    b = model.bias.item()
    print(f'权重为：{w},偏置为：{b}')
    # 可视化 1.损失图 2.源数据分布图 3.预测结果图
    plt.figure(figsize=(6,6),dpi=150)
    plt.plot(range(1,epochs+1),loss_list)
    plt.xlabel('训练轮数')
    plt.ylabel('MSE损失值')
    plt.title('训练损失图')
    plt.show()

    plt.figure(figsize=(6,6),dpi=150)
    plt.scatter(x,y,label='真实数据',color='red')
    y_true = coef * x + 11.4
    y_pre = model(x)
    print(y_true)
    print(y_pre)
    plt.plot(x,y_pre.detach(),label='预测结果',color='blue')
    plt.plot(x,y_true.detach(),label='真实结果',color='green')
    plt.legend()
    plt.grid()
    plt.title('预测结果图')
    plt.show()




if __name__ == '__main__':
    model_train()