import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr, kendalltau, skew, kurtosis, shapiro, normaltest, anderson
import statsmodels.api as sm
import statsmodels.formula.api as smf
from matplotlib.font_manager import FontProperties

# 1. 导入必要的库
# pandas - 数据操作
# numpy - 数值计算
# matplotlib - 数据可视化
# seaborn - 数据可视化，基于matplotlib
# scipy.stats - 统计分析
# statsmodels - 统计模型
# matplotlib.font_manager - 设置字体

# 设置中文字体
font_path = 'C:/Windows/Fonts/simhei.ttf'  # 这里是SimHei字体路径
font_prop = FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 2. 读取数据文件
file_path = 'D:/py/LearnPython/data0.xlsx'
data = pd.read_excel(file_path)

# 3. 生成描述性统计信息
descriptive_stats = data.describe()
print("描述性统计信息：")
print(descriptive_stats)

# 计算偏度和峰度
# 偏度：衡量数据分布的不对称程度
# 峰度：衡量数据分布的尖峰程度
skewness = data.apply(skew)
kurt = data.apply(kurtosis)
print("\n偏度：")
print(skewness)
print("\n峰度：")
print(kurt)

# 4. 计算相关性矩阵和皮尔森相关系数
# 皮尔森相关系数：衡量两个变量线性相关的程度
correlation_matrix = data.corr(method='pearson')
print("\n相关性矩阵（皮尔森相关系数）：")
print(correlation_matrix)

# 5. 可视化数据
# 相关性热图
plt.figure(figsize=(12, 10))  # 设置图形尺寸
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
# annot=True：显示每个单元格上的数值
# cmap='coolwarm'：颜色映射
# vmin=-1, vmax=1：颜色映射的范围
plt.title('相关性热图（皮尔森相关系数）', fontproperties=font_prop)
plt.show()

# 散点图矩阵
sns.pairplot(data)  # 绘制散点图矩阵
plt.show()

# 箱线图
plt.figure(figsize=(12, 6))  # 设置图形尺寸
sns.boxplot(data=data)
plt.title('箱线图', fontproperties=font_prop)
plt.show()

# 直方图和密度图
# 密度图
data.plot(kind='density', subplots=True, layout=(4, 4), sharex=False, figsize=(12, 12))
# kind='density'：绘制密度图
# subplots=True：为每个变量绘制单独的子图
# layout=(4, 4)：子图布局为4行4列
# sharex=False：子图不共享x轴
plt.suptitle('密度图', fontproperties=font_prop)
plt.show()

# 直方图
data.hist(bins=30, figsize=(15, 10))
# bins=30：直方图的柱数
plt.suptitle('直方图', fontproperties=font_prop)
plt.show()

# QQ图
plt.figure(figsize=(12, 6))  # 设置图形尺寸
for i, column in enumerate(data.columns, 1):
    plt.subplot(2, 4, i)  # 设置子图布局为2行4列
    sm.qqplot(data[column], line='s', ax=plt.gca())
    plt.title(f'QQ图 - {column}', fontproperties=font_prop)
plt.tight_layout()
plt.show()

# 6. 计算其他统计系数
# 斯皮尔曼相关系数
# 斯皮尔曼相关系数：衡量两个变量单调相关的程度
spearman_corr = data.corr(method='spearman')
print("斯皮尔曼相关系数矩阵：")
print(spearman_corr)

# 肯德尔相关系数
# 肯德尔相关系数：衡量两个变量一致性和顺序的相关程度
kendall_corr = data.corr(method='kendall')
print("肯德尔相关系数矩阵：")
print(kendall_corr)

# 计算各变量之间的具体相关系数和p值
def calculate_correlations(data):
    methods = ['pearson', 'spearman', 'kendall']
    correlation_results = {}
    for method in methods:
        corr_matrix = data.corr(method=method)
        # 计算p值矩阵
        p_values = data.corr(method=lambda x, y: pearsonr(x, y)[1]) - np.eye(len(data.columns))
        correlation_results[method] = (corr_matrix, p_values)
    return correlation_results

correlation_results = calculate_correlations(data)

for method, (corr_matrix, p_values) in correlation_results.items():
    print(f"{method.capitalize()} 相关系数矩阵：")
    print(corr_matrix)
    print(f"{method.capitalize()} 相关系数的 p 值矩阵：")
    print(p_values)

# 可视化不同相关系数
fig, axes = plt.subplots(1, 3, figsize=(18, 5))  # 设置子图布局为1行3列
methods = ['pearson', 'spearman', 'kendall']

for i, method in enumerate(methods):
    sns.heatmap(correlation_results[method][0], annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=axes[i])
    axes[i].set_title(f'{method.capitalize()} 相关系数热图', fontproperties=font_prop)

plt.show()
