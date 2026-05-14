"""
案例:
    筛选垃圾邮箱的字典.

回顾: 机器学习开发流程.
    1. 读取数据.
    2. 数据的预处理.
    3. 特征工程.
        特征提取, 特征预处理(归一化, 标准化), 特征降维, 特征提取, 特征组合.
    4. 模型训练.
    5. 模型预测.
    6. 模型评估.

特征降维:
    概述/目的:
        减少特征, 用来降低模型出现过拟合的情况(降低风险)
    思路:
        低方差法, 会设置一个方差阈值, 小于该阈值的列, 都会被删除掉, 只保留区别较大的字段, 更容易分析出结果.
"""

# 导包.
from sklearn.feature_selection import VarianceThreshold
import pandas as pd


# 1. 读取数据, 查看维度.
df = pd.read_csv('./data/垃圾邮件分类数据.csv')
print(df.shape) # (971, 25734)  -> (行, 列)

# 2. 创建 低方差对象.
transfer = VarianceThreshold(threshold=1)
# 3. 处理特征, 筛选出特征在0.01以上的 列.
x_new = transfer.fit_transform(df)

# 4. 打印处理后的 维度.
print(x_new.shape)  # (971, 144)  -> (行, 列)
