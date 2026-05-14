"""
演示神经网络搭建流程.

深度学习案例的4个步骤:
    1. 准备数据.
    2. 搭建神经网络
    3. 模型训练
    4. 模型测试

神经网络搭建流程:
    1. 定义一个类, 继承: nn.Module
    2. 在__init__()方法中, 搭建神经网络.
    3. 在 forward()方法中,完成: 前向传播.
"""

import torch
import torch.nn as nn
from torchsummary import summary

class TestModule(nn.Module):
    def __init__(self):
        super().__init__()
        #1. 初始化线性层
        self.layer_1 = nn.Linear(3, 3)
        self.layer_2 = nn.Linear(3, 2)
        self.layer_out = nn.Linear(2, 2)

        # 2. 参数初始化
        self._initialize_weights()

        # 3. 初始化激活函数
        self.sigmoid = nn.Sigmoid()
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=-1)

    # 定义一个初始化权重的函数，批量初始化
    def _initialize_weights(self):
        kaiming_layers_list = [self.layer_2,self.layer_out]
        for l in kaiming_layers_list:
        # self.modules() 是 nn.Module 类的一个方法，会返回一个生成器，递归地遍历当前模型中的所有模块
            if isinstance(l,nn.Linear):
            # isinstance() 是 Python 内置函数，用于检查对象是否是指定类的实例,这里判断当前模块 m 是否是 nn.Linear 类型（即线性层/全连接层）
                nn.init.kaiming_normal_(l.weight)
                if l.bias is not None:
                    nn.init.zeros_(l.bias)
        xavier_layers_list = [self.layer_1]
        for l in xavier_layers_list:
            if isinstance(l, nn.Linear):
                nn.init.xavier_normal_(l.weight)
                if l.bias is not None:
                    nn.init.zeros_(l.bias)

    def forward(self,x):
        # 第一层 加权求和 + sigmoid激活函数
        x = self.sigmoid(self.layer_1(x))
        # 第二层 加权求和 + relu激活函数
        x = self.relu(self.layer_2(x))
        # 第三次 加权求和 + softmax激活函数
        x = self.softmax(self.layer_out(x))
        return x




def model_test():
    # 简单训练一下初始的模型，打印一下参数数和各层参数值什么的
    model = TestModule()
    print(f'my_model: {model}')

    # 创建数据集
    test_data = torch.randn((5,3))
    print(f"初始数据：{test_data}")
    # 进行预测
    pre_result = model(test_data)
    print(f"预测结果:\n{pre_result}")

    # 打印模型参数（参数数量、每一层参数值）
    print('——'*35)
    summary(model,(5,3))
    # 打印每层参数
    print('——'*35)
    for name,params in model.named_parameters():
        print(f'name: {name}')
        print(f'param: {params} \n')




if __name__ == '__main__':
    model_test()