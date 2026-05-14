import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets import make_blobs

# 1. 生成模拟数据，包含多个簇
centers = [[1, 1], [-1, -1], [1, -1], [2, 2]]
X, _ = make_blobs(n_samples=500, centers=centers, cluster_std=0.6)

# 2. 自动估计带宽参数
bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)

# 3. 使用均值漂移进行聚类
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

# 4. 获取簇的数量
n_clusters = len(np.unique(labels))

# 5. 可视化聚类结果
plt.figure(figsize=(8, 6))

# 绘制每个簇的数据点
colors = plt.cm.get_cmap("viridis", n_clusters)
for k in range(n_clusters):
    members = labels == k
    plt.scatter(X[members, 0], X[members, 1], s=50, c=[colors(k)], label=f'簇 {k+1}')

# 绘制簇中心
plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], c='red', s=300, marker='x', label='簇中心')

plt.title(f'均值漂移聚类结果（簇的数量: {n_clusters}）')
plt.xlabel('特征 1')
plt.ylabel('特征 2')
plt.legend()
plt.show()
