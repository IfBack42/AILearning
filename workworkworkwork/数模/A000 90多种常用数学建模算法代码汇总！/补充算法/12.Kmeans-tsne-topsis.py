import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
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


# 4. TOPSIS 评价方法
def topsis(matrix):
    # 标准化决策矩阵
    norm_matrix = matrix / np.sqrt(np.sum(matrix ** 2, axis=0))

    # 理想解和负理想解
    ideal_best = np.max(norm_matrix, axis=0)  # 理想解
    ideal_worst = np.min(norm_matrix, axis=0)  # 负理想解

    # 计算每个客户到理想解和负理想解的距离
    dist_best = np.sqrt(np.sum((norm_matrix - ideal_best) ** 2, axis=1))
    dist_worst = np.sqrt(np.sum((norm_matrix - ideal_worst) ** 2, axis=1))

    # 计算综合得分（得分越高越接近理想解）
    score = dist_worst / (dist_best + dist_worst)

    return score


# 对每个类别分别计算 TOPSIS 评分
topsis_scores = {}

for i in range(n_clusters):
    # 取出每一类的数据
    cluster_data = data[data['Cluster'] == i].iloc[:, :-1].values  # 最后一列是 Cluster 列

    # 计算 TOPSIS 评分
    scores = topsis(cluster_data)
    topsis_scores[f'Cluster_{i + 1}'] = scores

    # 输出该类中客户的评分结果
    print(f"Cluster {i + 1} 的客户 TOPSIS 评分：")
    print(scores)

# 添加评分结果到原始数据中
for i in range(n_clusters):
    data.loc[data['Cluster'] == i, 'TOPSIS_Score'] = topsis_scores[f'Cluster_{i + 1}']

# 显示带有 TOPSIS 评分的数据
print(data.head())

