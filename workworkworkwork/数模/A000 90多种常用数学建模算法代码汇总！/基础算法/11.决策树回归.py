import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

# 加载数据
file_path = 'D:/py/LearnPython/data0.xlsx'
data = pd.read_excel(file_path)

# 分离输入和输出
X = data.iloc[:, :-1].values  # 输入特征
y = data.iloc[:, -1].values   # 输出目标

# 数据标准化
scaler = StandardScaler()  # 创建StandardScaler对象，用于将输入数据标准化
X_scaled = scaler.fit_transform(X)  # 对输入数据进行标准化

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 定义参数网格，用于穷举搜索
param_grid = {
    'max_depth': [3, 5, 7, 10],  # 树的最大深度
    'min_samples_split': [2, 5, 10],  # 内部节点再划分所需最小样本数
    'min_samples_leaf': [1, 2, 4]  # 叶子节点最少样本数
}

# 创建决策树回归模型
dt_model = DecisionTreeRegressor(random_state=42)

# 使用GridSearchCV进行参数优化
grid_search = GridSearchCV(estimator=dt_model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

# 获取最佳模型及其参数
best_dt = grid_search.best_estimator_
best_params = grid_search.best_params_

# 使用最佳模型进行预测
y_train_pred = best_dt.predict(X_train)
y_test_pred = best_dt.predict(X_test)

# 评估模型性能
def evaluate_model(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100  # 添加小常数避免除零
    return mse, r2, rmse, mae, mape

train_mse, train_r2, train_rmse, train_mae, train_mape = evaluate_model(y_train, y_train_pred)
test_mse, test_r2, test_rmse, test_mae, test_mape = evaluate_model(y_test, y_test_pred)

# 输出最佳模型性能和配置
print("Best model performance on training set:")
print(f"Train MSE: {train_mse:.4f}")
print(f"Train R2: {train_r2:.4f}")
print(f"Train RMSE: {train_rmse:.4f}")
print(f"Train MAE: {train_mae:.4f}")
print(f"Train MAPE: {train_mape:.4f}%")

print("\nBest model performance on test set:")
print(f"Test MSE: {test_mse:.4f}")
print(f"Test R2: {test_r2:.4f}")
print(f"Test RMSE: {test_rmse:.4f}")
print(f"Test MAE: {test_mae:.4f}")
print(f"Test MAPE: {test_mape:.4f}%")

print("Best model configuration:", best_params)

# 可视化训练集预测结果
plt.figure(figsize=(10, 6))
plt.plot(range(len(y_train)), y_train, color='blue', label='Actual Values')
plt.plot(range(len(y_train_pred)), y_train_pred, color='red', label='Predicted Values')
plt.title('Decision Tree Regression Prediction on Training Set')
plt.xlabel('Index')
plt.ylabel('Target Value')
plt.legend()
plt.grid(True)
plt.show()

# 可视化测试集预测结果
plt.figure(figsize=(10, 6))
plt.plot(range(len(y_test)), y_test, color='blue', label='Actual Values')
plt.plot(range(len(y_test_pred)), y_test_pred, color='red', label='Predicted Values')
plt.title('Decision Tree Regression Prediction on Test Set')
plt.xlabel('Index')
plt.ylabel('Target Value')
plt.legend()
plt.grid(True)
plt.show()

# 加载新的输入数据并进行预测
new_data_path = 'D:/py/LearnPython/data1.xlsx'
new_data = pd.read_excel(new_data_path)

# 去除特征名对新的输入数据进行标准化
new_data_scaled = scaler.transform(new_data.values)

# 使用最佳模型进行预测
new_predictions = best_dt.predict(new_data_scaled)

# 保存预测结果到新的Excel文件
output_path = 'D:/py/LearnPython/predictions_decision_tree.xlsx'
pd.DataFrame(new_predictions, columns=['Predicted Values']).to_excel(output_path, index=False)
print(f"Predictions saved to {output_path}")
