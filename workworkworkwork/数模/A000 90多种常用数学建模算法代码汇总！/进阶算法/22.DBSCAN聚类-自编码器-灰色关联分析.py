# 导入必要的库
import numpy as np  # 用于数值计算
import pandas as pd  # 用于数据操作
from sklearn.cluster import DBSCAN  # DBSCAN聚类算法
from sklearn.preprocessing import StandardScaler  # 用于数据标准化
from sklearn.metrics import pairwise_distances  # 用于计算灰色关联度
import matplotlib.pyplot as plt  # 用于数据可视化
from tensorflow.keras.models import Model  # 用于构建自编码器
from tensorflow.keras.layers import Dense, Input  # 用于定义神经网络的层

# 1. 生成随机数据
np.random.seed(42)  # 设置随机种子
X = np.random.rand(200, 4) * 100  # 生成4维随机数据（200个样本）

# 2. 数据标准化处理
scaler = StandardScaler()  # 实例化标准化工具
X_scaled = scaler.fit_transform(X)  # 对数据进行标准化处理

# 3. 使用DBSCAN进行聚类分析
dbscan = DBSCAN(eps=0.5, min_samples=5)  # 定义DBSCAN参数，eps为半径，min_samples为最小样本数
labels = dbscan.fit_predict(X_scaled)  # 进行DBSCAN聚类，并返回聚类标签

# 4. 可视化DBSCAN聚类结果
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap='plasma')  # 绘制二维散点图
plt.title('DBSCAN 聚类结果')  # 设置标题
plt.xlabel('特征 1')  # 设置x轴标签
plt.ylabel('特征 2')  # 设置y轴标签
plt.show()  # 显示图像

# 5. 使用自编码器进行降维
input_dim = X.shape[1]  # 获取输入维度
encoding_dim = 2  # 设置编码后的维度

# 定义自编码器结构
input_layer = Input(shape=(input_dim,))  # 输入层
encoder = Dense(encoding_dim, activation="relu")(input_layer)  # 编码层，ReLU激活函数
decoder = Dense(input_dim, activation="sigmoid")(encoder)  # 解码层
autoencoder = Model(inputs=input_layer, outputs=decoder)  # 构建自编码器模型

# 编译自编码器模型
autoencoder.compile(optimizer='adam', loss='mean_squared_error')  # 使用均方误差作为损失函数

# 训练自编码器
autoencoder.fit(X, X, epochs=50, batch_size=32, shuffle=True)  # 训练模型

# 使用编码器进行降维
encoder_model = Model(inputs=input_layer, outputs=encoder)  # 提取编码器部分
encoded_X = encoder_model.predict(X)  # 使用编码器对数据进行降维

# 6. 绘制降维后的数据
plt.scatter(encoded_X[:, 0], encoded_X[:, 1], c=labels, cmap='plasma')  # 绘制二维降维数据
plt.title('自编码器降维后的DBSCAN聚类结果')  # 设置标题
plt.show()  # 显示图像

# 7. 计算灰色关联度
# 定义灰色关联度计算函数
def grey_relation_analysis(X):
    reference = np.mean(X, axis=0)  # 计算参考序列（各维度的均值）
    grey_relation_grades = []
    for i in range(X.shape[0]):
        diff = np.abs(X[i] - reference)  # 计算差异序列
        max_diff = np.max(diff)
        min_diff = np.min(diff)
        grey_relation = (min_diff + 0.5 * max_diff) / (diff + 0.5 * max_diff)  # 灰色关联公式
        grey_relation_grades.append(np.mean(grey_relation))  # 计算各样本的灰色关联度
    return np.array(grey_relation_grades)

# 计算灰色关联度
grey_relation_grades = grey_relation_analysis(X)

# 将灰色关联度结果添加到数据框中
df = pd.DataFrame(X, columns=['Feature1', 'Feature2', 'Feature3', 'Feature4'])
df['Cluster'] = labels  # 添加聚类标签
df['Grey Relation'] = grey_relation_grades  # 添加灰色关联度分数
print(df.head())  # 打印前几行数据
