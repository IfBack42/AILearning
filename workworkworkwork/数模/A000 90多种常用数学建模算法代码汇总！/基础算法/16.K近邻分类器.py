import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. 加载鸢尾花数据集
iris = datasets.load_iris()
X = iris.data  # 特征数据（花萼长度、花萼宽度、花瓣长度、花瓣宽度）
y = iris.target  # 类别标签

# 2. 将数据集划分为训练集和测试集，80% 用于训练，20% 用于测试
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 数据标准化处理（KNN 对特征尺度敏感，因此进行标准化）
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. 创建 KNN 分类器，选择 K=5（邻居数为5）
knn = KNeighborsClassifier(n_neighbors=5)

# 5. 训练 KNN 模型
knn.fit(X_train_scaled, y_train)

# 6. 对测试集进行预测
y_pred = knn.predict(X_test_scaled)

# 7. 评估模型性能
accuracy = accuracy_score(y_test, y_pred)
print(f"模型准确率: {accuracy:.2f}")

# 输出混淆矩阵和分类报告
print("混淆矩阵:")
print(confusion_matrix(y_test, y_pred))

print("\n分类报告:")
print(classification_report(y_test, y_pred))
