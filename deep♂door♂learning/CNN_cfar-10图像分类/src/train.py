"""
在模型训练中，以下参数最好显式定义为全局变量或配置参数：
    1. 数据相关参数
        batch_size: 批次大小
        learning_rate: 学习率
        num_epochs: 训练轮次
        input_shape: 输入图像尺寸
    2. 模型架构参数
        in_channels: 输入通道数
        num_classes: 分类数量
        dropout_rate: Dropout比率
    3. 优化器参数
        optimizer_type: 优化器类型(Adam, SGD等)
        weight_decay: 权重衰减系数
        momentum: 动量参数(如使用SGD)
    4. 训练控制参数
        shuffle: 是否打乱数据
        device: 训练设备(CPU/GPU)
        save_interval: 模型保存间隔
    5. 评估相关参数
        validation_split: 验证集比例
        metrics: 评估指标
"""


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import time

from utils.create_dataset import create_dataset
from model.Image_model import Image_model

Batch_size = 64
Input_dim = 3
Output_dim = 10
Learning_rate = 1e-3
Epoches = 50


def train():
    # 1.加载数据集
    train_data,_ = create_dataset("../data")
    # 2.创建数据加载器
    data_loader = DataLoader(
        train_data,
        batch_size=Batch_size,   # 增大批量大小
        shuffle=True,
        num_workers=4,           # 根据CPU核心数调整
        pin_memory=True,         # GPU加速
        persistent_workers=True,
        prefetch_factor=2        # 预加载
    )
    # 3.初始化模型
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Image_model(Input_dim,Output_dim)
    model = model.to(device)
    # 4.创建损失函数对象
    criterion = nn.CrossEntropyLoss()
    # 5.创建优化器对象
    optimizer = optim.Adam(model.parameters(),lr=Learning_rate)

    # 6.开始每轮的循环
    for epoch in range(Epoches):
        # 转换模型状态
        model.train()
        # 定义变量记录 每轮总损失, 每轮预测正确样本个数, 每轮总样本数, 训练(开始)时间
        total_loss, total_correct, total_sample, start = 0.0, 0, 0, time.time()
        for x,y in data_loader: # 每次循环自动拿到一批数据
            # 将张量放到gpu训练
            x, y = x.to(device), y.to(device)

            # 1.模型预测
            pre_result = model(x)
            # 2.计算损失
            loss = criterion(pre_result,y)
            # 3.梯度清零
            optimizer.zero_grad()
            # 4.反向传播
            loss.backward()
            # 5.梯度更新
            optimizer.step()

            """
            记录这几个参数：
                1. 预测正确的个数，算准确率不必多说
                2. 每批次样本个数：每批损失是取得平均损失，使用平均损失*样本数得到 批次总损失 ，再得到 每轮总损失
                3. 每轮总损失再除以样本总数，得到每轮平均损失
            """
            # 记录总损失
            total_loss += loss.item() * (len(y))

            # 记录每批正确率
            pre_result = torch.argmax(pre_result, dim=-1)
            total_correct += (pre_result == y).sum() # 每批总正确个数

            # 记录每批样本个数，用于计算每轮平均损失、每轮正确率
            total_sample += len(y)

        # 打印每轮训练信息
        print(f'epoch: {epoch + 1}, loss: {total_loss / total_sample:.5f}, acc:{total_correct / total_sample:.2f}, time:{time.time() - start:.2f}s')

    # 保存模型
    torch.save(model.state_dict(), './model/image_model.pth')

if __name__ == '__main__':
    train()








