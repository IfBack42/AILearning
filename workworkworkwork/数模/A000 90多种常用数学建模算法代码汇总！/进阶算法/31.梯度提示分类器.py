# 导入必要的库
import numpy as np  # 用于数值计算
import pandas as pd  # 用于数据处理
from sklearn.model_selection import train_test_split  # 数据集划分工具
from sklearn.preprocessing import StandardScaler  # 数据标准化工具
from sklearn.ensemble import GradientBoostingClassifier  # 梯度提升分类器
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report  # 评估指标
import matplotlib.pyplot as plt  # 数据可视化工具

# 1. 读取数据
data_path = 'D:/py/LearnPython/分类模型/juleidata.xlsx'  # 设置数据路径
data = pd.read_excel(data_path)  # 读取Excel文件中的数据

# 2. 数据预处理
# 假设最后一列是目标变量Y，其他列是特征X
X = data.iloc[:, :-1].values  # 输入特征（所有列，除了最后一列）
Y = data.iloc[:, -1].values  # 输出（目标变量，最后一列）

# 数据标准化
scaler = StandardScaler()  # 创建一个标准化对象
X_scaled = scaler.fit_transform(X)  # 对特征数据进行标准化处理

# 将数据集划分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

# 3. 构建梯度提升分类器
gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)  # 构建梯度提升分类器

# 4. 训练模型
gbc.fit(X_train, Y_train)  # 使用训练集训练模型

# 5. 模型评估与预测
Y_train_pred = gbc.predict(X_train)  # 对训练集进行预测
Y_test_pred = gbc.predict(X_test)  # 对测试集进行预测

# 6. 计算分类评价指标
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    """评估模型性能"""
    accuracy = accuracy_score(Y_true, Y_pred)  # 计算准确率
    conf_matrix = confusion_matrix(Y_true, Y_pred)  # 生成混淆矩阵
    class_report = classification_report(Y_true, Y_pred)  # 生成分类报告
    print(f"{dataset_type} - 准确率: {accuracy:.4f}")  # 打印准确率
    print(f"{dataset_type} - 混淆矩阵:\n{conf_matrix}")  # 打印混淆矩阵
    print(f"{dataset_type} - 分类报告:\n{class_report}\n")  # 打印分类报告

# 评估训练集和测试集的性能
evaluate_model(Y_train, Y_train_pred, "训练集")
evaluate_model(Y_test, Y_test_pred, "测试集")

# 7. 绘制重要特征图
importances = gbc.feature_importances_  # 获取特征的重要性分数
indices = np.argsort(importances)[::-1]  # 对特征的重要性进行排序

# 可视化特征重要性
plt.figure(figsize=(12, 6))
plt.title("Feature Importances")
plt.bar(range(X_train.shape[1]), importances[indices], align='center')
plt.xticks(range(X_train.shape[1]), [f'Feature {i}' for i in indices])  # 设置x轴为特征索引
plt.xlabel("Feature Index")
plt.ylabel("Importance")
plt.show()

# 8. 可视化预测结果
plt.figure(figsize=(14, 6))

# 训练集对比图
plt.subplot(1, 2, 1)  # 创建第一个子图
plt.scatter(Y_train, Y_train_pred, color='blue', alpha=0.5, label='预测值')  # 绘制散点图
plt.plot([Y_train.min(), Y_train.max()], [Y_train.min(), Y_train.max()], 'k--', lw=2, label='理想情况')  # 绘制理想参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('训练集: 预测值 vs. 真实值')  # 设置图表标题
plt.legend()  # 显示图例

# 测试集对比图
plt.subplot(1, 2, 2)  # 创建第二个子图
plt.scatter(Y_test, Y_test_pred, color='green', alpha=0.5, label='预测值')  # 绘制散点图
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2, label='理想情况')  # 绘制理想参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('测试集: 预测值 vs. 真实值')  # 设置图表标题
plt.legend()  # 显示图例

plt.tight_layout()  # 调整子图布局，避免重叠
plt.show()  # 显示图表
