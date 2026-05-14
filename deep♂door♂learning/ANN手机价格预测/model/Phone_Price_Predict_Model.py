"""
案例:
    ANN(人工神经网络)案例: 手机价格分类案例.

背景:
    基于手机的20列特征 -> 预测手机的价格区间(4个区间), 可以用机器学习做, 也可以用 深度学习做(推荐)

ANN案例的实现步骤:
    1. 构建数据集.
    2. 搭建神经网络.
    3. 模型训练.
    4. 模型测试.

优化思路:
    1. 优化方法从 SGD -> Adam
    2. 学习率从 0.001 -> 0.0001
    3. 对数据进行标准化.
    4. 增加网络的深度, 每层的神经元数量
    5. 调整训练的轮数
    6. ......
"""
import torch
import torch.nn as nn
from torchsummary import summary                # 模型结构可视化


class Phone_model(nn.Module):
    def __init__(self,input_dim,output_dim):
        super().__init__()
        # 初始化模型层
        self.linear_in = nn.Linear(input_dim,64)
        self.linear1 = nn.Linear(64,128)
        self.linear2 = nn.Linear(128,256)
        self.linear3 = nn.Linear(256,512)
        self.linear4 = nn.Linear(512,128)
        self.linear5 = nn.Linear(128,64)
        self.linear_out = nn.Linear(64,output_dim)

    def forward(self,x):
        # 输入层：加权求和 + ReLU
        x = torch.relu(self.linear_in(x))
        # 隐藏层 1-5：加权求和 + ReLU
        x = torch.relu(self.linear1(x))
        x = torch.relu(self.linear2(x))
        x = torch.relu(self.linear3(x))
        x = torch.relu(self.linear4(x))
        x = torch.relu(self.linear5(x))
        # 输出层：单线性层，因为多分类交叉熵损失函数自带softmax
        x = self.linear_out(x)
        return x


# 测试模型
if __name__ == '__main__':
    # 创建模型
    model = Phone_model(input_dim=20, output_dim=4)
    print("模型结构:")
    print(model)


    # 创建测试数据
    batch_size = 4
    test_input = torch.randn(batch_size, 20)
    print(f"测试数据: {test_input.shape}")

    # 测试前向传播
    model.eval()  # 设置为评估模式
    with torch.no_grad():  # 关闭梯度计算
        output = model(test_input)

    print(f"\n测试结果:")
    print(f"输入形状: {test_input.shape}")
    print(f"输出形状: {output.shape}")
    print(f"输出值: {output}")

    # 获取预测类别
    predicted_classes = torch.argmax(output, dim=1)
    print(f"预测类别: {predicted_classes}")

    print("模型参数：\n")
    print(summary(model, input_size=(batch_size, 20)))