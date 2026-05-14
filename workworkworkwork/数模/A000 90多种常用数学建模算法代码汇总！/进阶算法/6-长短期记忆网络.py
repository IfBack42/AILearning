# 导入必要的库
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
import matplotlib.pyplot as plt
import warnings

# 忽略警告信息
warnings.filterwarnings('ignore')

# 确保使用的是 TensorFlow 2.x
assert tf.__version__.startswith('2'), "请确保使用的是 TensorFlow 2.x 版本。"

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 请确保路径正确
data = pd.read_excel(data_path)

# 2. 数据预处理
# 将最后一列作为目标变量 Y，其余列作为特征 X
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values   # 目标变量

# 对特征进行标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 将数据扩展为 3D 形状以用于 LSTM
X_scaled = np.expand_dims(X_scaled, axis=2)  # 添加一个维度，以符合 LSTM 输入要求

print(f"特征维度: {X_scaled.shape[1]}")  # 输出特征维度
print(f"目标变量样本数: {Y.shape[0]}")   # 输出目标变量的样本数

# 3. 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.2, random_state=42
)

# 4. 定义 LSTM 网络
lstm_inputs = layers.Input(shape=(X_scaled.shape[1], 1), name='lstm_input')  # LSTM 接受 3D 输入
x = layers.LSTM(64, activation='tanh', return_sequences=True)(lstm_inputs)
x = layers.LSTM(32, activation='tanh')(x)
x = layers.Dense(32, activation='relu')(x)
lstm_outputs = layers.Dense(1, activation='linear')(x)  # 最后一层输出 1 个回归值

# 构建模型
lstm_model = Model(lstm_inputs, lstm_outputs, name='LSTM_regressor')
lstm_model.summary()

# 5. 编译模型
lstm_model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 6. 训练 LSTM 模型
history_lstm = lstm_model.fit(
    X_train, Y_train,
    validation_data=(X_test, Y_test),
    epochs=2000,
    batch_size=32,
    verbose=1
)

# 7. 模型评估
# 进行预测
Y_train_pred = lstm_model.predict(X_train).flatten()
Y_test_pred = lstm_model.predict(X_test).flatten()

# 计算评价指标
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    mse = mean_squared_error(Y_true, Y_pred)
    mae = mean_absolute_error(Y_true, Y_pred)
    r2 = r2_score(Y_true, Y_pred)
    evs = explained_variance_score(Y_true, Y_pred)
    print(f"{dataset_type} - MSE: {mse:.4f}")
    print(f"{dataset_type} - MAE: {mae:.4f}")
    print(f"{dataset_type} - R²: {r2:.4f}")
    print(f"{dataset_type} - EVS: {evs:.4f}\n")

print("LSTM 模型评价指标：")
evaluate_model(Y_train, Y_train_pred, "训练集")
evaluate_model(Y_test, Y_test_pred, "测试集")

# 8. 结果可视化
plt.figure(figsize=(14, 6))

# 训练集对比图
plt.subplot(1, 2, 1)
plt.scatter(Y_train, Y_train_pred, color='blue', alpha=0.5, label='预测值')
plt.plot(
    [Y_train.min(), Y_train.max()],
    [Y_train.min(), Y_train.max()],
    'k--',
    lw=2,
    label='理想情况'
)
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('训练集: 预测值 vs. 真实值')
plt.legend()

# 测试集对比图
plt.subplot(1, 2, 2)
plt.scatter(Y_test, Y_test_pred, color='green', alpha=0.5, label='预测值')
plt.plot(
    [Y_test.min(), Y_test.max()],
    [Y_test.min(), Y_test.max()],
    'k--',
    lw=2,
    label='理想情况'
)
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('测试集: 预测值 vs. 真实值')
plt.legend()

plt.tight_layout()
plt.show()
