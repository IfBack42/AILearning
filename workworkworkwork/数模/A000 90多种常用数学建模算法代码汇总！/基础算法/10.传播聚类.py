import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AffinityPropagation
from sklearn.datasets import make_blobs

# 1. 生成二维数据集，包含多个簇
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5, random_state=42)

# 2. 使用传播聚类进行聚类
ap = AffinityPropagation(random_state=42)
ap.fit(X)
labels = ap.labels_
cluster_centers_indices = ap.cluster_centers_indices_

# 获取簇的数量
n_clusters = len(cluster_centers_indices)

# 3. 可视化聚类结果
plt.figure(figsize=(8, 6))

# 绘制数据点
colors = plt.cm.get_cmap("viridis", n_clusters)
for k, col in enumerate(colors(range(n_clusters))):
    members = labels == k
    plt.scatter(X[members, 0], X[members, 1], s=50, c=[col], label=f'簇 {k+1}')

# 绘制簇中心
cluster_centers = X[cluster_centers_indices]
plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], c='red', s=300, marker='x', label='簇中心')

plt.title(f'传播聚类结果（簇的数量: {n_clusters}）')
plt.xlabel('特征 1')
plt.ylabel('特征 2')
plt.legend()
plt.show()
