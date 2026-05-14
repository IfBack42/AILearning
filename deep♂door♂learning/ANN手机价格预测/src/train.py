"""
模型训练函数
"""

import time                                     # 时间模块
import torch
import torch.nn as nn
import torch.optim as opt
from torch.utils.data import DataLoader         # 数据加载器.
from src.common import create_dataset
from model.Phone_Price_Predict_Model import Phone_model

def model_train(train_dataset,input_dim,output_dim):
    # 1.创建数据加载器       
    data_loader = DataLoader(train_dataset,batch_size=16,shuffle=True)
    # 2.创建神经网络模型
    model = Phone_model(input_dim, output_dim)
    # 3.定义损失函数
    criterion = nn.CrossEntropyLoss()
    # 4.创建优化器对象
    # optimizer = opt.SGD(model.parameters(),lr=0.01,momentum=0.9)
    optimizer = opt.Adam(model.parameters(),lr=1e-4)

    # 5.开始循环训练
    epoches = 150
    for epoch in range(epoches):
        # 记录训练时间
        start_time = time.time()
        # 定义变量记录损失与每轮迭代次数
        epoch_total_loss = 0
        iter_num = 0
        # 开始每轮的训练(训练轮数在dataloader中了)
        for x,y in data_loader: # x,y,为每批次的数据 即16条20列的特征 和16条4类的标签
            model.train() # 转换模型状态为训练模式
            result = model(x)
            # 老四样
            loss = criterion(result,y) # 计算损失
            epoch_total_loss += loss.item() * len(y) # 记录损失(因为每次迭代batch可能不同，所以乘一个batch数，后续再计算平均)
            optimizer.zero_grad() # 梯度清零
            loss.backward() # 反向传播
            optimizer.step() # 梯度更新
            iter_num += len(y) # 记录迭代次数
        # 输出损失变化情况
        print(f'第{epoch+1}轮平均损失：{epoch_total_loss / iter_num:.4f}')
        print(f'训练用时：{time.time() - start_time}')
    # 模型保存
    # torch.save(model.state_dict(),'../model/phone-price-model.pt')

if __name__ == '__main__':
    import sys
    print(sys.path)
    # train_dataset,test_dataset,input_dim,output_dim = create_dataset()
    # model_train(train_dataset,input_dim,output_dim)
