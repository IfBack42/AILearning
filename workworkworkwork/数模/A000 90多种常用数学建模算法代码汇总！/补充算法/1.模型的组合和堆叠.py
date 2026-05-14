import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# 1. 加载数据
file_path = r'D:\py\LearnPython\ceshi_water.xlsx'  # 请确保文件路径正确
data = pd.read_excel(file_path)

# 2. 假设前几列是输入，最后一列是输出
X = data.iloc[:, :-1]  # 输入特征：前几列
y = data.iloc[:, -1]   # 输出特征：最后一列

# 3. 将数据划分为训练集和测试集，测试集占比为30%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. 对输入数据进行标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # 标准化训练集
X_test = scaler.transform(X_test)        # 标准化测试集

# 5. 训练各个单独的模型
# 随机森林回归
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 梯度提升回归
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb.fit(X_train, y_train)

# 线性回归
lr = LinearRegression()
lr.fit(X_train, y_train)

# 6. 预测单个模型的结果
rf_pred = rf.predict(X_test)  # 随机森林预测
gb_pred = gb.predict(X_test)  # 梯度提升预测
lr_pred = lr.predict(X_test)  # 线性回归预测

# 7. 堆叠模型的实现
# 将随机森林和梯度提升作为第一层模型，线性回归作为最终的预测模型
estimators = [('rf', rf), ('gb', gb)]
stack = StackingRegressor(estimators=estimators, final_estimator=LinearRegression())
stack.fit(X_train, y_train)

# 8. 堆叠模型预测
stack_pred = stack.predict(X_test)

# 9. 计算每个模型的均方误差（MSE）
rf_mse = mean_squared_error(y_test, rf_pred)
gb_mse = mean_squared_error(y_test, gb_pred)
lr_mse = mean_squared_error(y_test, lr_pred)
stack_mse = mean_squared_error(y_test, stack_pred)

# 10. 打印各个模型的MSE结果
print(f"随机森林模型的MSE: {rf_mse:.4f}")
print(f"梯度提升模型的MSE: {gb_mse:.4f}")
print(f"线性回归模型的MSE: {lr_mse:.4f}")
print(f"堆叠模型的MSE: {stack_mse:.4f}")

# 11. 打印堆叠模型预测值与真实值的对比
predictions_comparison = pd.DataFrame({
    '真实值': y_test,
    '堆叠模型预测值': stack_pred
})
print(predictions_comparison.head())  # 显示前几行的预测结果
