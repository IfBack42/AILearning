import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.cluster import SpectralClustering
from sklearn.preprocessing import StandardScaler

# 1. 生成非凸形状数据集（例如：月牙形数据集）
X, y = make_moons(n_samples=300, noise=0.05, random_state=42)

# 2. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. 使用光谱聚类
n_clusters = 2  # 假设我们知道有两个簇
spectral = SpectralClustering(n_clusters=n_clusters, affinity='rbf', gamma=1.0, random_state=42)
labels = spectral.fit_predict(X_scaled)

# 4. 可视化聚类结果
plt.figure(figsize=(10, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap='viridis', marker='o')
plt.title('光谱聚类结果')
plt.xlabel('特征 1')
plt.ylabel('特征 2')
plt.show()

# 5. 输出聚类结果
print("聚类标签：", labels)
