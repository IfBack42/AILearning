# 导入必要的库
import numpy as np  # 用于数值计算
import pandas as pd  # 用于数据处理
from sklearn.model_selection import train_test_split  # 用于数据集划分
from sklearn.preprocessing import StandardScaler  # 数据标准化
from sklearn.kernel_ridge import KernelRidge  # 核岭回归
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report  # 评估指标
import matplotlib.pyplot as plt  # 用于绘图
from sklearn.multiclass import OneVsRestClassifier  # 用于处理多分类任务

# 1. 读取数据
data_path = 'D:/py/LearnPython/分类模型/juleidata.xlsx'  # 数据路径
data = pd.read_excel(data_path)  # 读取Excel文件中的数据

# 2. 数据预处理
# 假设最后一列是目标变量Y，其他列是特征X
X = data.iloc[:, :-1].values  # 取数据的所有行，除了最后一列作为特征X
Y = data.iloc[:, -1].values  # 取最后一列作为目标变量Y

# 数据标准化
scaler = StandardScaler()  # 创建一个标准化对象
X_scaled = scaler.fit_transform(X)  # 对特征数据进行标准化

# 将数据集划分为训练集和测试集，80%为训练集，20%为测试集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

# 3. 构建核岭回归分类器
# 核岭回归在默认情况下用于回归，但我们将其用于分类问题
kr_classifier = OneVsRestClassifier(KernelRidge(kernel='rbf', alpha=1.0))  # 使用RBF核，alpha控制正则化

# 4. 使用训练集进行模型训练
kr_classifier.fit(X_train, Y_train)  # 在训练集上训练核岭回归模型

# 5. 进行预测
Y_train_pred = kr_classifier.predict(X_train)  # 在训练集上进行预测
Y_test_pred = kr_classifier.predict(X_test)  # 在测试集上进行预测

# 6. 评估模型性能
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    """用于评估模型性能的函数"""
    accuracy = accuracy_score(Y_true, Y_pred)  # 计算准确率
    conf_matrix = confusion_matrix(Y_true, Y_pred)  # 计算混淆矩阵
    class_report = classification_report(Y_true, Y_pred)  # 生成分类报告
    print(f"{dataset_type} - 准确率: {accuracy:.4f}")  # 打印准确率
    print(f"{dataset_type} - 混淆矩阵:\n{conf_matrix}")  # 打印混淆矩阵
    print(f"{dataset_type} - 分类报告:\n{class_report}\n")  # 打印分类报告

# 评估训练集和测试集的性能
evaluate_model(Y_train, Y_train_pred, "训练集")  # 在训练集上评估模型性能
evaluate_model(Y_test, Y_test_pred, "测试集")  # 在测试集上评估模型性能

# 7. 绘制训练集与测试集预测结果对比图
plt.figure(figsize=(14, 6))  # 创建绘图窗口，设置窗口大小

# 训练集对比图
plt.subplot(1, 2, 1)  # 创建一个子图，表示训练集的对比图
plt.scatter(Y_train, Y_train_pred, color='blue', alpha=0.5, label='预测值')  # 绘制训练集真实值与预测值的散点图
plt.plot([Y_train.min(), Y_train.max()], [Y_train.min(), Y_train.max()], 'k--', lw=2, label='理想情况')  # 绘制参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('训练集: 预测值 vs. 真实值')  # 设置图标题
plt.legend()  # 显示图例

# 测试集对比图
plt.subplot(1, 2, 2)  # 创建第二个子图，表示测试集的对比图
plt.scatter(Y_test, Y_test_pred, color='green', alpha=0.5, label='预测值')  # 绘制测试集真实值与预测值的散点图
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2, label='理想情况')  # 绘制参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('测试集: 预测值 vs. 真实值')  # 设置图标题
plt.legend()  # 显示图例

plt.tight_layout()  # 自动调整子图之间的布局
plt.show()  # 显示图像
