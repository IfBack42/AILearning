"""
案例:
    演示特征降维, 降低模型出现 过拟合的风险.

思路: 相关系数法
    皮尔逊相关系数: 计算x的累加和, y的累加和, x*y的累加和, x²累加和, y²累加和  稍显繁琐.
    斯皮尔曼相关系数: 通过自定义等级(个数), 来实现管理(特征筛选)的动作.

相关系数法快速复习:
    1. 它关注两个变量之间的关系, 可以用于:
        - 特征 vs 标签: 判断某个特征和预测目标是否有关.
        - 特征 vs 特征: 判断两个特征是否高度重复.
    2. 它属于 特征选择: 最终通常是删除弱相关特征或删除高度重复特征中的一个.
    3. 适合连续数值特征的快速探索, 例如:
        - Iris鸢尾花: 花瓣长度和花瓣宽度常常高度相关.
        - California Housing: 房屋位置、收入、房龄与房价的关系.
        - Diabetes糖尿病回归: BMI、血压等指标与疾病进展的关系.

皮尔逊相关系数:
    公式:
        r = Cov(X, Y) / (std(X) * std(Y))
    适合:
        线性关系, 例如 x 越大 y 越大, 且接近一条直线.

斯皮尔曼相关系数:
    思路:
        先把数值转成排名, 再计算排名之间的相关性.
    适合:
        单调关系, 排名关系, 或异常值较多的数据.

相关系数取值:
    接近 1: 强正相关.
    接近 -1: 强负相关.
    接近 0: 简单相关性弱.

常用阈值经验:
    |r| < 0.1: 很弱.
    0.3 <= |r| < 0.5: 中等.
    |r| >= 0.8: 很强, 特征之间可能重复.

注意:
    相关系数容易漏掉组合关系和非线性关系.
    例如 y = x ** 2 这种抛物线关系, Pearson和Spearman都可能接近0.
"""

# 导包
import pandas as pd
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
print(f'鸢尾花特征矩阵维度: {x.shape}')
print(f'花萼长度前5个值: {x1[:5]}')
print(f'花瓣长度前5个值: {x2[:5]}')

# 3. 计算相关系数.
# statistic参数: 相关系数; pvalue越小, 说明该相关关系越不像偶然出现.
pearson_result = pearsonr(x1, x2)
spearman_result = spearmanr(x1, x2)
print(f'皮尔逊相关系数: {pearson_result}')
print(f'斯皮尔曼相关系数: {spearman_result}')

# 4. 补充: 用DataFrame查看所有特征两两之间的相关系数矩阵.
feature_names = ['花萼长度', '花萼宽度', '花瓣长度', '花瓣宽度']
df = pd.DataFrame(x, columns=feature_names)
print('鸢尾花特征之间的皮尔逊相关系数矩阵:')
print(df.corr(method='pearson'))

# 5. 补充: 演示相关系数的盲区, y = x ** 2 是强非线性关系, 但线性/单调相关可能很弱.
curve_x = pd.Series([-3, -2, -1, 0, 1, 2, 3])
curve_y = curve_x ** 2
print(f'抛物线关系 Pearson: {pearsonr(curve_x, curve_y)}')
print(f'抛物线关系 Spearman: {spearmanr(curve_x, curve_y)}')
