"""
模型测试评估
"""
import torch
import torch.nn
from torch.utils.data import DataLoader
from src.common import create_dataset
from model.Phone_Price_Predict_Model import Phone_model

def eval(test_dataset,input_dim,output_dim):
    # 创建模型对象
    model = Phone_model(input_dim,output_dim)
    # 加载模型参数
    model.load_state_dict(torch.load("../model/phone-price-model.pt"))
    # 创建数据加载器
    data_loader = DataLoader(test_dataset,batch_size=16,shuffle=False) # 测试集不打乱顺序
    # 定义变量记录预测正确数
    correct_num = 0
    # 循环进行预测
    for x,y in data_loader:
        model.eval() # 切换模型状态
        pre_result = model(x)
        print(f'输出结果：{pre_result}')
        # 预测结果为4类结果的神经网络计算值，没有转化为概率且保留最大的概率，需要argmax选取最大值为分类结果
        pre_result = torch.argmax(pre_result,dim=1) # dim=1表示按行
        print(f"预测结果：{pre_result}")
        print(f'真实结果：{y}')
        print('——'*15)
        correct_num += (pre_result==y).sum()
    print(f'准确率：{correct_num/len(test_dataset):.4f}')

if __name__ == '__main__':
    _,test_dataset,input_dim,output_dim = create_dataset()
    eval(test_dataset,input_dim, output_dim)