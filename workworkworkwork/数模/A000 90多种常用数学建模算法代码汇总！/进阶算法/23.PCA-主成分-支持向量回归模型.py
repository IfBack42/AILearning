# 导入必要的库
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA  # 主成分分析
from sklearn.cluster import KMeans  # K-means 聚类
from sklearn.svm import SVR  # 支持向量机回归
from sklearn.model_selection import train_test_split  # 数据集划分
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score  # 评估回归模型
import matplotlib.pyplot as plt  # 用于绘制图形

# 1. 生成随机数据集
np.random.seed(42)
data = np.random.rand(200, 5)  # 假设有200个样本，每个样本5个特征

# 2. 生成与特征数据相关的目标变量 Y
Y = np.sin(np.sum(data, axis=1))  # 生成目标变量 Y

# 3. 数据降维 (PCA)
pca = PCA(n_components=2)  # 将数据降至2维
data_pca = pca.fit_transform(data)  # 应用 PCA

# 4. K-means 聚类
kmeans = KMeans(n_clusters=3, random_state=42)  # K-means 聚类，聚成3类
labels = kmeans.fit_predict(data_pca)  # 聚类，并生成每个样本的标签

# 可视化聚类结果
plt.scatter(data_pca[:, 0], data_pca[:, 1], c=labels, cmap='viridis', marker='o')
plt.title("K-means 聚类结果 (PCA 降维后)")
plt.xlabel("主成分 1")
plt.ylabel("主成分 2")
plt.show()

# 5. 针对每个聚类分别建立回归模型并计算误差
for cluster in np.unique(labels):
    # 筛选出该聚类下的数据
    X_cluster = data[labels == cluster]
    Y_cluster = Y[labels == cluster]

    # 将该类别的数据集划分为训练集和测试集
    X_train, X_test, Y_train, Y_test = train_test_split(X_cluster, Y_cluster, test_size=0.2, random_state=42)

    # 建立SVR回归模型
    svr_model = SVR(kernel='rbf', C=100, gamma=0.1)
    svr_model.fit(X_train, Y_train)  # 在训练集上训练模型

    # 对测试集进行预测
    Y_pred = svr_model.predict(X_test)

    # 计算该聚类的误差
    mse = mean_squared_error(Y_test, Y_pred)  # 均方误差
    mae = mean_absolute_error(Y_test, Y_pred)  # 平均绝对误差
    r2 = r2_score(Y_test, Y_pred)  # R²得分

    # 输出该类的误差
    print(f"聚类 {cluster} 的回归模型误差:")
    print(f"均方误差 (MSE): {mse:.4f}")
    print(f"平均绝对误差 (MAE): {mae:.4f}")
    print(f"R²得分: {r2:.4f}\n")

# 结束
