import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.datasets import make_blobs
from matplotlib.patches import Ellipse

# 1. 生成二维数据集，数据点分布在三个不同的高斯簇中
X, y_true = make_blobs(n_samples=500, centers=3, cluster_std=[1.0, 2.5, 0.5], random_state=42)

# 2. 使用高斯混合模型进行聚类
gmm = GaussianMixture(n_components=3, covariance_type='full', random_state=42)
gmm.fit(X)
labels = gmm.predict(X)

# 获取每个高斯分布的均值、协方差
means = gmm.means_
covariances = gmm.covariances_


# 3. 可视化聚类结果以及每个簇的椭圆形边界
def plot_ellipse(mean, cov, ax):
    v, w = np.linalg.eigh(cov)  # 特征值分解
    v = 2.0 * np.sqrt(2.0) * np.sqrt(v)  # 放大椭圆的半径
    u = w[0] / np.linalg.norm(w[0])  # 椭圆方向

    angle = np.arctan(u[1] / u[0])  # 椭圆旋转的角度
    angle = 180.0 * angle / np.pi  # 弧度制转为角度制

    ell = Ellipse(mean, v[0], v[1], 180.0 + angle, color='red', alpha=0.3)
    ax.add_patch(ell)


# 绘制聚类结果
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis')

# 绘制每个簇的椭圆形边界
ax = plt.gca()
for mean, cov in zip(means, covariances):
    plot_ellipse(mean, cov, ax)

plt.title('高斯混合模型聚类结果')
plt.xlabel('特征 1')
plt.ylabel('特征 2')
plt.show()
