import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. 加载鸢尾花数据集，使用四个特征
iris = datasets.load_iris()
X = iris.data  # 使用所有四个特征：花萼长度、花萼宽度、花瓣长度、花瓣宽度
y = iris.target  # 标签

# 2. 将数据集划分为训练集和测试集，80% 用于训练，20% 用于测试
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 数据标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. 使用支持向量机分类模型（RBF 核函数）
svm_rbf = SVC(kernel='rbf', random_state=42, gamma='auto')  # 使用 RBF 核函数
svm_rbf.fit(X_train_scaled, y_train)  # 训练模型

# 5. 对测试集进行预测
y_pred = svm_rbf.predict(X_test_scaled)

# 6. 评估模型性能
accuracy = accuracy_score(y_test, y_pred)
print(f"模型准确率: {accuracy:.2f}")

# 输出混淆矩阵和分类报告
print("混淆矩阵:")
print(confusion_matrix(y_test, y_pred))

print("\n分类报告:")
print(classification_report(y_test, y_pred))
