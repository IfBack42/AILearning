# 导入必要的库
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
import statsmodels.api as sm  # 导入广义估计方程（GEE）模型
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

# 3. 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

# 将训练集和测试集转换为DataFrame（GEE模型需要DataFrame格式）
X_train_df = pd.DataFrame(X_train, columns=[f'feature_{i}' for i in range(X_train.shape[1])])
X_test_df = pd.DataFrame(X_test, columns=[f'feature_{i}' for i in range(X_test.shape[1])])

# 4. 构建GEE模型
# 创建一个用于标记群体的“组变量”（假设没有自然的组变量，可以自己创建一个虚拟变量）
group = np.arange(len(X_train)) // 10  # 每10个样本一组

# 创建模型，并设置工作相关性结构（比如独立相关性结构）
gee_model = sm.GEE(Y_train, sm.add_constant(X_train_df), groups=group, family=sm.families.Gaussian())

# 5. 训练模型
gee_result = gee_model.fit()  # 拟合模型
print(gee_result.summary())  # 打印模型结果

# 6. 模型评估与预测
Y_train_pred = gee_result.predict(sm.add_constant(X_train_df))  # 训练集预测
Y_test_pred = gee_result.predict(sm.add_constant(X_test_df))  # 测试集预测

# 7. 计算4个详细的数字评价指标
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

# 8. 可视化训练集和测试集的预测值 vs. 真实值
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
