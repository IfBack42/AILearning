"""
案例:
    演示特征降维, 降低模型出现 过拟合的风险.

思路: 相关系数法
    皮尔逊相关系数: 计算x的累加和, y的累加和, x*y的累加和, x²累加和, y²累加和  稍显繁琐.
    斯皮尔曼相关系数: 通过自定义等级(个数), 来实现管理(特征筛选)的动作.
"""

# 导包
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from sklearn.datasets import load_iris


# 1. 读取鸢尾花数据.
x, y = load_iris(return_X_y=True)

# 2. x(特征) -> 花萼的长, 花萼的宽, 花瓣的长, 花瓣的宽.
# 因为 皮尔逊相关系数, 斯皮尔曼相关系数, 都是计算 两个变量 之间的相关系数.
# 故此 从x(特征) 抽取两列, 来分析这两列的相关系数.
x1 = x[:, 0]    # 花萼的长
x2 = x[:, 2]    # 花瓣的长
print(x)
print(x1)
print(x2)

# 3. 计算相关系数.
# 皮尔逊相关系数: PearsonRResult(statistic=-0.11756978413300204, pvalue=0.15189826071144746)
# statistic参数: 相关系数
print(f'皮尔逊相关系数: {pearsonr(x1, x2)}')

# 斯皮尔曼相关系数: SignificanceResult(statistic=-0.166777658283235, pvalue=0.04136799424884587)
# statistic参数: 相关系数
print(f'斯皮尔曼相关系数: {spearmanr(x1, x2)}')