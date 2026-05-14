import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'
data = pd.read_excel(data_path)

# 假设数据的最后一列是标签，前几列是输入特征
# 如果数据格式不同，你可以调整这里的列选取方式
X = data.iloc[:, :-1].values  # 输入特征（前几列）

# 2. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. 使用 KMeans 聚类
n_clusters = 2 # 假设我们希望分成 3 类
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X_scaled)

# 获取聚类标签和簇中心
labels = kmeans.labels_  # 每个点的簇标签
centroids = kmeans.cluster_centers_  # 每个簇的质心

# 将聚类结果加入到原始数据中
data['Cluster'] = labels

# 4. 可视化聚类结果
# 如果输入特征是二维的，我们可以直接进行可视化，如果是多维数据，可以使用 t-SNE 等降维工具
if X_scaled.shape[1] == 2:
    plt.figure(figsize=(10, 6))
    plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap='viridis', marker='o')
    plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='red', marker='x')  # 绘制簇中心
    plt.title('KMeans 聚类结果')
    plt.xlabel('特征1')
    plt.ylabel('特征2')
    plt.show()
else:
    print("输入数据维度超过二维，可以使用降维工具（如t-SNE）来可视化。")

# 5. 输出聚类结果
print("聚类结果：")
print(data.head())

# 保存聚类结果为 Excel 文件
output_path = 'D:/py/LearnPython/kmeans_output.xlsx'
data.to_excel(output_path, index=False)
print(f"聚类结果已保存到：{output_path}")
