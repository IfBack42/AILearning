"""
案例:
    鸢尾花案例, 演示 pca分析法 实现 特征降维.

pca分析法介绍:
    概述:
        它属于降维的思路一种, 可以接收 小数 -> 表示保留特征的比例.   可以接收整数 -> 表示保留特征的个数.
    弊端:
        pca不适合处理大批次的特征数据(例如: 有几W个特征列...), 可以先用 低方差法删除保留重要特征, 然后结合pca分析法实现.
"""

# 导包.
from sklearn.decomposition import PCA   # pca分析法对象.
from sklearn.datasets import load_iris  # 加载鸢尾花数据集


# 1. 读取数据, 获取x, y
x, y = load_iris(return_X_y=True)   # x -> 特征矩阵, y -> 标签,
# print(x)  # 特征: 花萼长, 花萼宽,花瓣长度,花瓣宽度.
# print(y)  # 1个(三分法)

# 2. 创建pca对象, 保留特征.
# 如果是整数, 就保留: n个特征.
# pca = PCA(n_components=2)
# # 3. 训练, 获取x_new
# x_new = pca.fit_transform(x)
# # 4. 查看处理后的信息.
# print(x_new)

# 如果是小数, 就: 保留: n%
pca = PCA(n_components=0.6)
# 3. 训练, 获取x_new
x_new = pca.fit_transform(x)
# 4. 查看处理后的信息.
print(x_new)