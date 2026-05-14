import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from matplotlib import font_manager

# 设置自定义字体（替换为你的字体路径）
font_path = 'C:/Users/12595/Desktop/STZHONGS.TTF'  # 自定义字体路径
font_prop = font_manager.FontProperties(fname=font_path)

# 1. 加载鸢尾花数据集，只选择前两个特征
iris = datasets.load_iris()
X = iris.data[:, :2]  # 只选择前两个特征（花萼长度和花萼宽度）
y = iris.target  # 标签

# 2. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. 将数据集划分为训练集和测试集，80% 用于训练，20% 用于测试
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 4. 使用支持向量机分类模型（线性核函数）
svm_linear = SVC(kernel='linear', random_state=42)
svm_linear.fit(X_train, y_train)

# 5. 使用支持向量机分类模型（RBF 核函数）
svm_rbf = SVC(kernel='rbf', random_state=42)
svm_rbf.fit(X_train, y_train)

# 6. 对测试集进行预测（线性核）
y_pred_linear = svm_linear.predict(X_test)

# 7. 对测试集进行预测（RBF 核）
y_pred_rbf = svm_rbf.predict(X_test)

# 8. 评估模型性能（线性核）
print("线性核 SVM 模型性能：")
print(f"准确率: {accuracy_score(y_test, y_pred_linear):.2f}")
print("混淆矩阵:")
print(confusion_matrix(y_test, y_pred_linear))
print("\n分类报告:")
print(classification_report(y_test, y_pred_linear))

# 9. 评估模型性能（RBF 核）
print("\nRBF 核 SVM 模型性能：")
print(f"准确率: {accuracy_score(y_test, y_pred_rbf):.2f}")
print("混淆矩阵:")
print(confusion_matrix(y_test, y_pred_rbf))
print("\n分类报告:")
print(classification_report(y_test, y_pred_rbf))

# 10. 可视化两个特征的分类边界
def plot_svc_decision_boundary(model, X, y, title):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, alpha=0.8)
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, edgecolor='k', s=50)
    plt.title(title, fontproperties=font_prop)
    plt.xlabel('花萼长度', fontproperties=font_prop)
    plt.ylabel('花萼宽度', fontproperties=font_prop)
    plt.legend(*scatter.legend_elements(), title="类别", prop=font_prop)
    plt.show()

# 绘制线性核 SVM 的分类边界
plot_svc_decision_boundary(svm_linear, X_train, y_train, '线性核 SVM 分类边界')

# 绘制 RBF 核 SVM 的分类边界
plot_svc_decision_boundary(svm_rbf, X_train, y_train, 'RBF 核 SVM 分类边界')
