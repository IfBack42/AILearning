"""
梯度下降法完成波士顿房价预测案例

线性回归： 有监督学习，有标签，有特征，标签连续
分类：
    一元线性回归：一个特征列，一个标签列
    y = w * x + b
    多元线性回归：多个特征列，多个标签列
    y = w1 * x1 + w2 * x2 + w3 * x3 ... + wn * xn  =  w转置 * x + b
模型评估 ：预测值与真实值误差
    1.最小二乘：样本误差平方和
    2.均方误差（MSE）：样本误差平方和/样本总数
    3.均方根误差（RMSE）：样本误差平方和/样本总数 整体开根
    4.平均绝对误差（MAE）：样本误差绝对值和/样本总数
损失函数最小化：
    1.正规方程法：构建特征矩阵 和 标签矩阵，通过使误差最小的矩阵求导法 直接算出权重
    2.梯度下降法： 全梯度下降（Full Gradient Descent） 随机梯度下降法（SGD） 小批量梯度下降（Mini Batch） 随即平均梯度下降法（SAG）
"""
# 导包
# from sklearn.datasets import load_boston # 已弃用
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error,mean_absolute_error
from sklearn.linear_model import SGDRegressor # 线性回归梯度下降法
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge,RidgeCV # 正则化
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1.加载数据
raw_df = pd.read_csv("./boston_data.csv", sep="\\s+", skiprows=22, header=None)
target = raw_df.values[1::2, 2]
features = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]]) # hstack 水平拼接 数组
print(f'特征形状：{features.shape}')
print(f'标签形状：{target.shape}')

# 2.数据预处理（干净的，不需要）

# 3. 特征工程
# 3.1 训练集分割
x_train,x_test,y_train,y_test = train_test_split(features,target,train_size=0.8)
# 3.2 特征预处理(标准化)
transfer = StandardScaler()
x_train = transfer.fit_transform(x_train)
x_test = transfer.transform(x_test)

# 4.1 模型训练
estimator = SGDRegressor(
    loss='squared_error', # 损失函数默认MSE
    max_iter=1000, # 迭代次数
    fit_intercept=True, #计算截距，默认True，不用管
    eta0=0.01, # 初始学习率
    learning_rate='constant', # 学习率模式为常量，学习率不变
)                       # 线性回归梯度下降算法只支持随机梯度下降，没有小批量什么的
estimator.fit(x_train,y_train)
# 4.2 拿模型参数
print(f'权重：{estimator.coef_}')
print(f'偏置：{estimator.intercept_}')
# 4.3模型预测
pre_result = estimator.predict(x_test)

# 5 模型评估 模型评估不需要更换损失函数来计算这几个值，直接带入公式计算就行了
print(f'均方误差：{mean_squared_error(y_true=y_test,y_pred=pre_result)}')
print(f'均方根误差：{np.sqrt(mean_squared_error(y_true=y_test,y_pred=pre_result))}')
print(f'平均绝对误差：{mean_absolute_error(y_true=y_test,y_pred=pre_result)}')

plt.figure(figsize=(15,10))

# ------ 1. 实际值 vs 预测值散点图 ------
plt.subplot(2, 2, 1)
plt.scatter(y_test, pre_result, alpha=0.6)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')  # 对角线
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Actual vs Predicted")
plt.grid(True)
plt.show()