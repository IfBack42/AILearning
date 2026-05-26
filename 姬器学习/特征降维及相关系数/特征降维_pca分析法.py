"""
案例:
    鸢尾花案例, 演示 pca分析法 实现 特征降维.

pca分析法介绍:
    概述:
        它属于降维的思路一种, 可以接收 小数 -> 表示保留特征的比例.   可以接收整数 -> 表示保留特征的个数.
    弊端:
        pca不适合处理大批次的特征数据(例如: 有几W个特征列...), 可以先用 低方差法删除保留重要特征, 然后结合pca分析法实现.

PCA快速复习:
    1. PCA不是简单删列, 而是把原来的多个特征重新组合成更少的新特征.
    2. 新特征叫 主成分, 第1主成分保留的信息最多, 第2主成分次之.
    3. PCA属于 特征提取/特征变换: 降维后的列不再是原来的花萼长、花瓣宽等原始含义.
    4. 适合特征之间有冗余、想压缩维度或可视化的场景, 例如:
        - Iris鸢尾花: 4维压到2维画散点图.
        - Digits/MNIST手写数字: 64维/784维像素压缩.
        - 人脸图像: 高维像素压缩, 经典应用叫Eigenfaces.
        - Wine葡萄酒: 多个化学指标可能存在相关性.

核心原理:
    PCA会寻找数据变化最大的方向.
    方差越大的方向, 越能保留样本之间的差异, 信息量通常越大.

简化公式:
    1. 中心化:
        X_centered = X - mean(X)
    2. 计算协方差矩阵:
        Cov = X_centered.T @ X_centered / n
    3. 求特征值和特征向量:
        Cov @ v = lambda @ v
       v 是主成分方向, lambda 表示该方向保留的方差信息量.

超参:
    n_components:
        整数: 保留几个主成分, 如 PCA(n_components=2).
        小数: 保留多少累计方差信息, 如 PCA(n_components=0.95).
    常用选择:
        可视化: 2 或 3.
        建模压缩: 0.90, 0.95, 0.99, 再用验证集比较模型效果.

注意:
    PCA对特征尺度敏感, 通常要先做标准化 StandardScaler.
"""

# 导包.
from sklearn.decomposition import PCA   # pca分析法对象.
from sklearn.datasets import load_iris  # 加载鸢尾花数据集
from sklearn.preprocessing import StandardScaler


# 1. 读取数据, 获取x, y
x, y = load_iris(return_X_y=True)   # x -> 特征矩阵, y -> 标签,
# print(x)  # 特征: 花萼长, 花萼宽,花瓣长度,花瓣宽度.
# print(y)  # 1个(三分法)

# 2. PCA建议先标准化, 避免某个量纲大的特征因为方差大而主导结果.
x = StandardScaler().fit_transform(x)

# 3. 创建pca对象, 保留特征.
# 如果是整数, 就保留: n个主成分.
pca_2 = PCA(n_components=2)
x_new_2 = pca_2.fit_transform(x)
print(f'原始维度: {x.shape}')
print(f'保留2个主成分后的维度: {x_new_2.shape}')
print(f'2个主成分各自解释的方差比例: {pca_2.explained_variance_ratio_}')
print(f'2个主成分累计解释的方差比例: {pca_2.explained_variance_ratio_.sum():.4f}')

# 如果是小数, 就: 保留: n%
pca = PCA(n_components=0.95)
# 4. 训练, 获取x_new
x_new = pca.fit_transform(x)
# 5. 查看处理后的信息.
print(f'保留95%信息后的维度: {x_new.shape}')
print(f'实际保留的累计方差比例: {pca.explained_variance_ratio_.sum():.4f}')
print(f'降维后的前5行数据:\n{x_new[:5]}')
