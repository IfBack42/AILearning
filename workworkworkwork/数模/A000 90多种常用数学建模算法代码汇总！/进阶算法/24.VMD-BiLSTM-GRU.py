# 导入必要的库
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, Model
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 数据路径
data = pd.read_excel(data_path)  # 读取 Excel 文件中的数据

# 2. 数据预处理
# 假设最后一列是目标变量 Y，其他列是特征 X
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values   # 输出（目标变量）

# 3. 自定义 VMD 实现
def VMD(signal, alpha, tau, K, DC, init, tol):
    """
    Variational Mode Decomposition (VMD)

    参数:
        signal: 输入信号（一维数组）
        alpha: 惩罚因子
        tau: 复数域惩罚项的时间步长
        K: 模态数量
        DC: 是否包含直流分量（0 或 1）
        init: 初始化模式（0：全零，1：随机）
        tol: 收敛阈值

    返回:
        u: 模态函数集合
        omega: 中心频率集合
    """
    # 初始化
    N = len(signal)
    T = N
    t = np.arange(1, N + 1)
    freqs = t / T

    # 初始化 u, omega, lambda_hat
    u = np.zeros((K, N))
    u_hat = np.zeros((K, N), dtype=complex)
    omega = np.zeros(K)
    if init == 1:
        omega = 0.5 / K * np.arange(K)
    lambda_hat = np.zeros(N, dtype=complex)
    f_hat = np.fft.fft(signal)
    f_hat_plus = np.copy(f_hat)
    f_hat_plus[:N//2] = 0

    # 主循环
    u_diff = tol + 1
    n_iter = 0
    while (u_diff > tol) and (n_iter < 500):
        u_prev = np.copy(u_hat)
        n_iter += 1
        for k in range(K):
            # 计算残差
            sum_uk = np.sum(u_hat, axis=0) - u_hat[k, :]
            residual = f_hat - sum_uk - lambda_hat / 2

            # 更新 u_hat[k]
            denominator = 1 + alpha * (freqs - omega[k]) ** 2
            u_hat[k, :] = (residual) / denominator

            # 更新 omega[k]
            numerator = np.sum(freqs * np.abs(u_hat[k, :]) ** 2)
            denominator = np.sum(np.abs(u_hat[k, :]) ** 2) + 1e-8  # 防止除以零
            omega[k] = numerator / denominator

        # 更新 lambda_hat
        sum_u_hat = np.sum(u_hat, axis=0)
        lambda_hat += tau * (sum_u_hat - f_hat)

        # 计算收敛性
        u_diff = np.sum(np.abs(u_hat - u_prev) ** 2) / np.sum(np.abs(u_prev) ** 2)

    u = np.fft.ifft(u_hat, axis=1).real
    return u, omega

# 设置 VMD 参数（调整后）
alpha = 1000       # 惩罚因子，降低 alpha 值
tau = 0            # 噪声容忍度
K = 8              # 增加模态数为 8
DC = 0             # 是否包括直流分量
init = 1           # 初始化模式
tol = 1e-6         # 收敛阈值，增加精度

# 对每个特征进行 VMD 分解，并将模态作为新的特征
X_vmd = []

for i in range(X.shape[1]):
    signal = X[:, i]
    u, omega = VMD(signal, alpha, tau, K, DC, init, tol)
    # u 的形状为 (K, N)
    X_vmd.append(u)

# 将列表转换为数组，形状为 (特征数, K, N)
X_vmd = np.array(X_vmd)

# 调整形状，将模态展开到特征维度
# 目标形状为 (N, 特征数 * K)
X_vmd = X_vmd.transpose(2, 0, 1).reshape(X.shape[0], -1)

# 将 VMD 分解的模态特征与原始特征合并
X_combined = np.hstack((X, X_vmd))

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_combined)

# 将数据划分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.2, random_state=42)

# 将数据扩展为 3D 形状，适用于 LSTM/GRU
X_train = np.expand_dims(X_train, axis=2)
X_test = np.expand_dims(X_test, axis=2)

# 4. 构建 VMD-BiLSTM-GRU 模型（调整后）
def build_vmd_bilstm_gru_model(input_shape):
    inputs = layers.Input(shape=input_shape)

    # 双向 LSTM 层（增加神经元数量）
    bilstm = layers.Bidirectional(layers.LSTM(256, return_sequences=True))(inputs)
    bilstm = layers.BatchNormalization()(bilstm)
    bilstm = layers.Dropout(0.5)(bilstm)

    # GRU 层（增加神经元数量）
    gru = layers.GRU(128, return_sequences=False)(bilstm)
    gru = layers.BatchNormalization()(gru)
    gru = layers.Dropout(0.5)(gru)

    # 全连接层（增加层数和神经元数量）
    dense = layers.Dense(128, activation='relu')(gru)
    dense = layers.BatchNormalization()(dense)
    dense = layers.Dropout(0.5)(dense)

    dense = layers.Dense(64, activation='relu')(dense)
    dense = layers.BatchNormalization()(dense)
    dense = layers.Dropout(0.5)(dense)

    outputs = layers.Dense(1, activation='linear')(dense)

    model = Model(inputs=inputs, outputs=outputs)
    return model

# 5. 构建并编译模型（调整学习率）
input_shape = (X_train.shape[1], X_train.shape[2])  # 输入形状
model = build_vmd_bilstm_gru_model(input_shape)

# 使用 Huber 损失函数和 Adam 优化器（减小学习率）
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
              loss=tf.keras.losses.Huber(),
              metrics=['mae'])

# 打印模型结构
model.summary()

# 6. 训练模型（增加训练轮数，取消早停机制）
history = model.fit(X_train, Y_train,
                    epochs=500,
                    batch_size=16,
                    validation_split=0.2,
                    verbose=1)

# 7. 模型评估
def evaluate_model(model, X_test, Y_test, dataset_type="数据集"):
    Y_pred = model.predict(X_test).flatten()
    mse = mean_squared_error(Y_test, Y_pred)
    mae = mean_absolute_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)
    print(f"{dataset_type} - MSE: {mse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")
    return Y_pred

# 评估训练集和测试集性能
Y_train_pred = evaluate_model(model, X_train, Y_train, "训练集")
Y_test_pred = evaluate_model(model, X_test, Y_test, "测试集")

# 8. 绘制训练过程中的损失曲线
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='训练损失')
plt.plot(history.history['val_loss'], label='验证损失')
plt.title('模型训练过程中的损失曲线')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

# 9. 绘制训练集和测试集的预测值 vs. 真实值
def plot_predictions(Y_true, Y_pred, dataset_type="数据集"):
    plt.figure(figsize=(6, 6))
    plt.scatter(Y_true, Y_pred, color='blue', alpha=0.5)
    plt.plot([Y_true.min(), Y_true.max()], [Y_true.min(), Y_true.max()], 'k--', lw=2)
    plt.xlabel('真实值')
    plt.ylabel('预测值')
    plt.title(f'{dataset_type}: 预测值 vs. 真实值')
    plt.show()

# 训练集预测图
plot_predictions(Y_train, Y_train_pred, "训练集")

# 测试集预测图
plot_predictions(Y_test, Y_test_pred, "测试集")
