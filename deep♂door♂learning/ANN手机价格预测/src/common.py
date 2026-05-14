"""
定义通用函数
"""

import torch
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset      # 数据集对象.
from sklearn.model_selection import train_test_split    # 训练集和测试集的划分

def create_dataset():
    # 数据 -> Tensor -> 张量数据集 -> 数据加载器
    # 1.加载数据集
    data = pd.read_csv("../data/手机价格预测.csv")
    # data.info() # 0-19：特征列 ，20：标签列
    # 2.划分特征列和标签列
    x = data.iloc[:,0:-1]
    y = data.iloc[:,-1]
    # print(x.head(),y.head())
    # 3.转化int类型特征为float
    x = x.astype(np.float32)
    # 划分训练集测试集
    x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=42,stratify=y)
    # 分别标准化测试集训练集数据防止数据泄露
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test) # 不能让测试集重新fit,否则让每一条数据看到测试集的统计信息
    # 创建张量数据集
    train_dataset = TensorDataset(torch.from_numpy(x_train),torch.tensor(y_train.values))
    test_dataset = TensorDataset(torch.from_numpy(x_test),torch.tensor(y_test.values))

    # 返回训练集数据、测试集数据、输入维度、输出维度
    return train_dataset,test_dataset,x.shape[1],len(np.unique(y))


if __name__ == '__main__':
    train_dataset,test_dataset,input_dim,output_dim = create_dataset()
    # 分别查看这四个结果
    print(f'train_dataset:{train_dataset}')
    print(f'test_dataset:{test_dataset}')
    print(f'input_dim:{input_dim}')
    print(f'output_dim:{output_dim}')
