# 导入必要的库
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process import GaussianProcessRegressor  # GPR模型
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C  # GPR的核函数
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
import matplotlib.pyplot as plt

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 数据路径
data = pd.read_excel(data_path)  # 读取Excel文件中的数据

# 2. 数据预处理
# 假设最后一列是目标变量Y，其他列是特征X
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values  # 输出（目标变量）

# 数据标准化
scaler = StandardScaler()  # 初始化标准化器
X_scaled = scaler.fit_transform(X)  # 对X进行标准化

# 将数据划分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

# 3. 构建高斯过程回归模型
# 定义核函数，使用常量核和径向基函数核（RBF kernel）
kernel = C(1.0, (1e-4, 1e1)) * RBF(1.0, (1e-4, 1e1))  # 核函数的常数和RBF的尺度

gpr_model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)  # 使用核函数构建高斯过程模型

# 4. 训练模型
gpr_model.fit(X_train, Y_train)

# 5. 模型评估与预测
Y_train_pred, sigma_train = gpr_model.predict(X_train, return_std=True)  # 训练集预测和标准差
Y_test_pred, sigma_test = gpr_model.predict(X_test, return_std=True)  # 测试集预测和标准差

# 6. 计算4个详细的数字评价指标
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    """评估模型性能"""
    mse = mean_squared_error(Y_true, Y_pred)  # 均方误差
    mae = mean_absolute_error(Y_true, Y_pred)  # 平均绝对误差
    r2 = r2_score(Y_true, Y_pred)  # R²得分
    evs = explained_variance_score(Y_true, Y_pred)  # 解释方差
    print(f"{dataset_type} - MSE: {mse:.4f}")
    print(f"{dataset_type} - MAE: {mae:.4f}")
    print(f"{dataset_type} - R²: {r2:.4f}")
    print(f"{dataset_type} - EVS: {evs:.4f}\n")

# 评估训练集和测试集的性能
evaluate_model(Y_train, Y_train_pred, "训练集")
evaluate_model(Y_test, Y_test_pred, "测试集")

# 7. 绘制训练集和测试集的预测值 vs. 真实值
plt.figure(figsize=(14, 6))

# 训练集对比图
plt.subplot(1, 2, 1)
plt.scatter(Y_train, Y_train_pred, color='blue', alpha=0.5, label='预测值')
plt.plot([Y_train.min(), Y_train.max()], [Y_train.min(), Y_train.max()], 'k--', lw=2, label='理想情况')
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('训练集: 预测值 vs. 真实值')
plt.legend()

# 测试集对比图
plt.subplot(1, 2, 2)
plt.scatter(Y_test, Y_test_pred, color='green', alpha=0.5, label='预测值')
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2, label='理想情况')
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('测试集: 预测值 vs. 真实值')
plt.legend()

plt.tight_layout()
plt.show()
