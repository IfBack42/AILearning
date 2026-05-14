"""
演示 欠拟合 正好拟合 过拟合 L1正则化 L3正则化 效果图

欠拟合：模型在训练集和测试集表现都不好 -> 增加特征，提高模型复杂度
正好拟合：模型在训练集和测试集表现都好
过拟合： 模型在训练集表表现好，在测试集表现不好

欠拟合原因：
    学习到数据特征过少
解决： 从数据、模型、算法角度解决
    1.添加其他特征
    2.“组合”“泛化”“相关性”特征
    3.添加多项式特征

过拟合原因：
    原始特征过多，存在嘈杂特征，模型兼顾太多数据点导致模型复杂
解决：
    1.重新清洗数据，对过多异常点数据、不纯数据进行清洗
    2.增大训练集数据量
    3.正则化，减少异常特征影响 或 对复杂度影响大的特征 的影响 -> 在损失函数中添加正则化项
    4.减少特征维度，防止维度灾难：特征多、样本少，导致学习不充分，泛化能力差，

L1 L2 正则化：
    介绍：基于惩罚系数修改特征列权重，惩罚系数越大，修改力度越大，对应权重越小
    L1 进行特征选取，将高维特征权重置0，过滤掉导致模型过拟合的小权重
    L2 进行系数收缩，使权重趋近0，平均分配权重，防止多重共线性，实际开发中在正确特征选取后使用L2正则化
    生动形象：
        夯哥去爬山，带了个包，装了 充电宝 水 雨伞 鞋子 衣服 面包
        L1：丢掉不必要的 -> 如果当天去当天回且天气晴朗 -> 不带雨伞鞋子 -> 权重置零
        L2：换个大包 -> 东西没变，空间占比小了 -> 权重变小

"""

from sklearn.metrics import mean_squared_error,mean_absolute_error
from sklearn.linear_model import LinearRegression # 线性回归梯度下降法
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge,RidgeCV,Lasso # 正则化
import numpy as np
import matplotlib.pyplot as plt

# 1. 定义函数演示欠拟合
def under_fitting():
    # 1.1 固定随机种子
    np.random.seed(114)
    # 1.2 生成特征标签数据
    x = np.random.uniform(-3,3,size=100) # 生成一维数组，100个值
    X = x.reshape(-1,1) # 重构成100行1列的二维数组
    y = 0.5 * x ** 3 + x + np.random.normal(0,1,size=100) # 用线性方程拟合一个二次方程
    # 1.3 训练模型
    estimator = LinearRegression()
    estimator.fit(X,y)
    # 1.4 模型预测
    pre_result = estimator.predict(X)
    # 1.5 模型评估
    print(f'权重：{estimator.coef_}')
    print(f'偏置：{estimator.intercept_}')
    print(f"MSE：{mean_squared_error(y,pre_result)}")
    print(f"MAE：{mean_absolute_error(y,pre_result)}")
    print(f"RMSE：{np.sqrt(mean_squared_error(y,pre_result))}")
    # 1.6 可视化
    plt.figure()
    plt.plot(x,pre_result,color='red')
    plt.scatter(x,y)
    plt.show()

# 2. 定义函数演示过拟合
def over_fitting():
    # 2.1 固定随机种子
    np.random.seed(23)
    # 2.2 生成特征标签数据
    x = np.random.uniform(-3,3,size=100)    # 生成一维数组，100个值
    X = x.reshape(-1,1)                          # 重构成100行1列的二维数组
    y = 0.5 * x ** 2 + x + np.random.normal(0,1,size=100) # 用线性方程拟合一个二次方程
    # 2.3 增加更多模型特征列，增加模型复杂度,达到过拟合效果 👉（其实是一种特征工程，挖掘特征之间的联系，捕获更多特征）
    X3 = np.hstack([X,X**2,X**3,X**4,X**5,X**6,X**7,X**8,X**9]) # 行stack，将n个 👉数组👈 进行水平拼接，拼接后数组列数等于n，行数不变
    print(X,X3,sep='\n')
    # 2.4 训练模型
    estimator = LinearRegression()
    estimator.fit(X3,y)
    # 2.5 模型预测
    pre_result = estimator.predict(X3)
    # 2.6 模型评估
    print(f'权重：{estimator.coef_}')
    print(f'偏置：{estimator.intercept_}')
    print(f"MSE：{mean_squared_error(y,pre_result)}")
    print(f"MAE：{mean_absolute_error(y,pre_result)}")
    print(f"RMSE：{np.sqrt(mean_squared_error(y,pre_result))}")
    # 2.7 可视化
    plt.figure()  # np.sort(x)：将原始特征值按从小到大的顺序排列
                  # np.argsort(x)：获取排序后的索引序列
    plt.plot(np.sort(x),pre_result[np.argsort(x)],color='red')  # 这是一种单变量问题专用可视化，仅适合单驱动因素的可视化
    plt.scatter(x,y)
    plt.show()
# 3. 正好拟合
def just_fitting():
    # 3.1 固定随机种子
    np.random.seed(23)
    # 3.2 生成特征标签数据
    x = np.random.uniform(-3,3,size=100)    # 生成一维数组，100个值
    X = x.reshape(-1,1)                          # 重构成100行1列的二维数组
    y = 0.5 * x ** 2 + x + np.random.normal(0,1,size=100) # 用线性方程拟合一个二次方程
    # 3.3 增加模型特征列，增加模型复杂度 👉（其实是一种特征工程，挖掘特征之间的联系，捕获更多特征）
    X3 = np.hstack([X,X ** 2]) # 行stack，将n个 👉数组👈 进行水平拼接，拼接后数组列数等于n，行数不变
    print(X,X3,sep='\n')
    # 3.4 训练模型
    estimator = LinearRegression()
    estimator.fit(X3,y)
    # 3.5 模型预测
    pre_result = estimator.predict(X3)
    # 3.6 模型评估
    print(f'权重：{estimator.coef_}')
    print(f'偏置：{estimator.intercept_}')
    print(f"MSE：{mean_squared_error(y,pre_result)}")
    print(f"MAE：{mean_absolute_error(y,pre_result)}")
    print(f"RMSE：{np.sqrt(mean_squared_error(y,pre_result))}")
    # 3.7 可视化
    plt.figure()  # np.sort(x)：将原始特征值按从小到大的顺序排列
                  # np.argsort(x)：获取排序后的索引序列
    plt.plot(np.sort(x),pre_result[np.argsort(x)],color='red')  # 这是一种单变量问题专用可视化，仅适合单驱动因素的可视化
    plt.scatter(x,y)
    plt.show()
# 4. L1正则化
def L1_regularzation():
    # 4.1 固定随机种子
    np.random.seed(23)
    # 4.2 生成特征标签数据
    x = np.random.uniform(-3, 3, size=100)  # 生成一维数组，100个值
    X = x.reshape(-1, 1)  # 重构成100行1列的二维数组
    y = 0.5 * x ** 2 + x + np.random.normal(0, 1, size=100)  # 用线性方程拟合一个二次方程
    # 4.3 增加更多模型特征列，增加模型复杂度,达到过拟合效果 👉（其实是一种特征工程，挖掘特征之间的联系，捕获更多特征）
    X3 = np.hstack(
        [X, X ** 2, X ** 3, X ** 4, X ** 5, X ** 6, X ** 7, X ** 8, X ** 9, X ** 10])  # 行stack，将n个 👉数组👈 进行水平拼接，拼接后数组列数等于n，行数不变
    print(X, X3, sep='\n')
    # 4.4 训练模型 模型选取正则化Lasso对象
    estimator = Lasso(alpha=1.0) #Lasso模型使用坐标下降，不需要设置学习率什么的，大数据集可以手动设置SGDRegressor+L1正则化
    estimator.fit(X3, y)
    # 4.5 模型预测
    pre_result = estimator.predict(X3)
    # 4.6 模型评估
    print(f'权重：{estimator.coef_}')
    print(f'偏置：{estimator.intercept_}')
    print(f"MSE：{mean_squared_error(y, pre_result)}")
    print(f"MAE：{mean_absolute_error(y, pre_result)}")
    print(f"RMSE：{np.sqrt(mean_squared_error(y, pre_result))}")
    # 4.7 可视化
    plt.figure()  # np.sort(x)：将原始特征值按从小到大的顺序排列
    # np.argsort(x)：获取排序后的索引序列
    plt.plot(np.sort(x), pre_result[np.argsort(x)], color='red')  # 这是一种单变量问题专用可视化，仅适合单驱动因素的可视化
    plt.scatter(x, y)
    plt.show()

# 5. L2正则化
def L2_regularzation():
    # 5.1 固定随机种子
    np.random.seed(23)
    # 5.2 生成特征标签数据
    x = np.random.uniform(-3, 3, size=100)  # 生成一维数组，100个值
    X = x.reshape(-1, 1)  # 重构成100行1列的二维数组
    y = 0.5 * x ** 2 + x + np.random.normal(0, 1, size=100)  # 用线性方程拟合一个二次方程
    # 5.3 增加更多模型特征列，增加模型复杂度,达到过拟合效果 👉（其实是一种特征工程，挖掘特征之间的联系，捕获更多特征）
    X3 = np.hstack(
        [X, X ** 2, X ** 3, X ** 4, X ** 5, X ** 6, X ** 7, X ** 8, X ** 9,
         X ** 10])  # 行stack，将n个 👉数组👈 进行水平拼接，拼接后数组列数等于n，行数不变
    print(X, X3, sep='\n')
    # 5.4 训练模型 模型选取正则化Lasso对象
    estimator = Ridge(alpha=100.0)
    estimator.fit(X3, y)
    # 5.5 模型预测
    pre_result = estimator.predict(X3)
    # 5.6 模型评估
    print(f'权重：{estimator.coef_}')
    print(f'偏置：{estimator.intercept_}')
    print(f"MSE：{mean_squared_error(y, pre_result)}")
    print(f"MAE：{mean_absolute_error(y, pre_result)}")
    print(f"RMSE：{np.sqrt(mean_squared_error(y, pre_result))}")
    # 5.7 可视化
    plt.figure()  # np.sort(x)：将原始特征值按从小到大的顺序排列
    # np.argsort(x)：获取排序后的索引序列
    plt.plot(np.sort(x), pre_result[np.argsort(x)], color='red')  # 这是一种单变量问题专用可视化，仅适合单驱动因素的可视化
    plt.scatter(x, y)
    plt.show()


if __name__ == '__main__':
    # under_fitting()
    just_fitting()
    # over_fitting()
    # L1_regularzation()
    # L2_regularzation()
