import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

# 1. 生成模拟数据，包含多个簇和噪声点
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4, random_state=0)

# 添加一些噪声点
X = np.vstack([X, np.random.uniform(low=-3, high=3, size=(50, 2))])

# 2. 数据标准化
X_scaled = StandardScaler().fit_transform(X)

# 3. 使用 DBSCAN 进行聚类
db = DBSCAN(eps=0.3, min_samples=10).fit(X_scaled)
labels = db.labels_

# 获取核心点的索引
core_samples_mask = np.zeros_like(labels, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True

# 获取不同的聚类标签
unique_labels = set(labels)

# 4. 可视化聚类结果
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
plt.figure(figsize=(10, 7))

for k, col in zip(unique_labels, colors):
    if k == -1:
        # 噪声点
        col = [0, 0, 0, 1]  # 黑色
    class_member_mask = (labels == k)

    # 绘制核心点
    xy = X_scaled[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=14)

    # 绘制边界点
    xy = X_scaled[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)

plt.title('DBSCAN 聚类结果（包括噪声点）')
plt.xlabel('特征 1')
plt.ylabel('特征 2')
plt.show()
