"""
逻辑回归：
    有监督学习：有特征有标签，且标签是离散的
    适用于二分类
    原理：
        （简单理解）：把线性回归处理后的预测值 -> 通过sigmoid函数映射到（0，1）之间，根据阈值结合概率划分==分类。
        定义上：使线性回归公式符合泊松分布，求得似然函数，使用最大似然估计和梯度下降算得最大概率时的权重系数
        损失函数：极大似然估计函数的负数形式
回顾机器学习项目流程：
    1.加载数据
    2.数据预处理
    3.特征工程
    4.模型训练
    5.模型预测
    6.模型评估
LogisticRegressor参数： 默认将样本中少数类别作为正类
    penalty(正则化类型)：'l1', 'l2', 'elasticnet', None 注意None没有引号
    C (正则化强度)：正则化强度的倒数，越小表示正则化越强，默认1
    solver (优化算法)：可选值: 'newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'
        'newton-cg'	牛顿共轭梯度法	中小数据	L2
        'liblinear'	坐标下降法（LIBLINEAR）	小数据	L1, L2
        'lbfgs'	有限内存拟牛顿法（L-BFGS）	中小数据（默认）	L2
        'sag'	随机平均梯度下降法	大数据	L2
        'saga'	随机平均梯度下降改进版	大数据	L1, L2, Elastic-Net
            默认情况：用 'lbfgs'（平衡速度和稳定性）。
            需要 L1 正则化：小数据用 'liblinear'，大数据用 'saga'。
            大数据 + 弹性网络：只能用 'saga'。
            多分类问题：优先选 'newton-cg'、'lbfgs' 或 'saga'。
    max_iter (最大迭代次数)，默认100

LogisticRegressor参数：penalty正则化类型（"L1"，"L2"，"elasticnet",None）;C正则化强度；
solver优化算法（'newton-cg','lbfgs','liblinear','sag','saga');max_iter最大迭代次数。

"""

#导包
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression # 逻辑回归模型
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#1.加载数据
data = pd.read_csv('./data/breast-cancer-wisconsin.csv')
# data0.info()

#2. 数据预处理
#2.1 替换空值
data.replace('?',np.nan,inplace=True)
#2.2缺失值处理
data.dropna(axis=0,inplace=True)
# data0.info()

#3 特征预处理
#3.1特征提取
x = data.iloc[:,1:-1] #所有行，第一列到最后一列，包左不包右
y = data.iloc[:,-1]
# print(x.shape,y.shape)
#3.2 划分训练集
x_train,x_test,y_train,y_test = train_test_split(x,y,train_size=0.8,random_state=23)
#3.3 归一化（老师讲的标准化，但是数据挺干净而且量纲一样，我觉得归一化方便）
transfor = MinMaxScaler()
x_train = transfor.fit_transform(x_train)
x_test = transfor.transform(x_test)

#4 模型训练 + 预测
estimator = LogisticRegression(penalty=None) # 数据很干净，量纲也一样，正则化干嘛啊
estimator.fit(x_train,y_train)
y_pre = estimator.predict(x_test)
print(y_pre)
print(estimator.coef_,estimator.intercept_)

#5 模型评估
print(f"正确率：{estimator.score(x_test,y_test)}") #这俩原理是一样的，score是调用一下预测再和y_test比较，accuracy是直接比较
print(f"正确率：{accuracy_score(y_pre,y_test)}")
# 逻辑回归用准确率有瑕疵，必须得知到底是谁预测失误，所以需要用到混淆矩阵：精确率，召回率，F1 score，ROC曲线，AUC值









