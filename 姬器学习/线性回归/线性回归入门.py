"""
线性回归介绍：
    用线性公式来描述多个自变量（特征）和一个因变量（标签）的关系，对其关系进行建模，基于特征预测标签
线性回归属于有监督学习，有特征有标签，标签连续
分类：
    一元线性回归：一个特征列 + 一个标签列
    多元线性回归：多个特征列 + 一个标签列
公式：
    一元线性回归：
        y = kx + b => wx + b
        # 数学中 k 叫斜率，b 叫截距， 机器学习中 w 叫权重（weight），b 叫偏置（Bias）
    多元线性回归：
        y = w1x1 +w2x2 + ... + wnxn +b
          = w矩阵的转置（一列） * x的矩阵（一行） + b
"""
# 导报
from sklearn.linear_model import LinearRegression

# 准备数据
x_train = [[160],[166],[172],[174],[180]]
y_train = [56.3,60.6,65.1,68.5,75]
x_test = [[176]]
# 数据预处理 不需要
# 特征工程 不需要
# 模型训练
estimator = LinearRegression()
estimator.fit(x_train,y_train)
print(f'权重：{estimator.coef_}')
print(f'偏置：{estimator.intercept_}')
#模型预测
pre = estimator.predict(x_test)
print(pre)
#模型评估
