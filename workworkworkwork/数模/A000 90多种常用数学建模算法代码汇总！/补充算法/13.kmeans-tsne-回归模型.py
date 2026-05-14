import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'
data = pd.read_excel(data_path)

# 假设数据的最后一列是输出，前几列是输入
X = data.iloc[:, :-1].values  # 输入特征（前几列）
y = data.iloc[:, -1].values  # 输出标签（最后一列）

# 1. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. KMeans 聚类
n_clusters = 3  # 假设分成 3 类
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(X_scaled)

# 将聚类结果加入到原始数据中
data['Cluster'] = cluster_labels

# 3. t-SNE 降维并可视化
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)

plt.figure(figsize=(10, 6))
for i in range(n_clusters):
    plt.scatter(X_tsne[cluster_labels == i, 0], X_tsne[cluster_labels == i, 1], label=f'Cluster {i + 1}')
plt.title('t-SNE 降维结果')
plt.xlabel('t-SNE 维度 1')
plt.ylabel('t-SNE 维度 2')
plt.legend()
plt.show()

# 4. 线性回归模型
regression_models = {}
mse_scores = {}

for i in range(n_clusters):
    # 获取属于当前簇的数据
    cluster_data = data[data['Cluster'] == i]
    X_cluster = cluster_data.iloc[:, :-2].values  # 排除输出列和聚类列
    y_cluster = cluster_data.iloc[:, -2].values  # 输出标签

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X_cluster, y_cluster, test_size=0.2, random_state=42)

    # 训练线性回归模型
    reg = LinearRegression()
    reg.fit(X_train, y_train)

    # 预测和评估
    y_pred = reg.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    # 保存模型和评估结果
    regression_models[f'Cluster_{i + 1}'] = reg
    mse_scores[f'Cluster_{i + 1}'] = mse

    # 输出该类模型的 MSE
    print(f"Cluster {i + 1} 的线性回归模型的 MSE：{mse:.4f}")

# 输出每个类别的 MSE 评分
print("每个类别的 MSE 评分：", mse_scores)
