# 导入必要的库
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, Model
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
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
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 数据扩展为 3D 形状，以符合 CNN 的输入要求
X_scaled = np.expand_dims(X_scaled, axis=2)  # 将输入数据扩展为3D，以适应Conv1D层

# 将数据划分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

# 3. 构建多层卷积神经网络（CNN）
def build_cnn(input_shape):
    model = tf.keras.Sequential()

    # 第一层卷积层 + 池化层
    model.add(layers.Conv1D(64, kernel_size=3, activation='relu', padding='same', input_shape=input_shape))
    model.add(layers.MaxPooling1D(pool_size=2))

    # 第二层卷积层 + 池化层
    model.add(layers.Conv1D(128, kernel_size=3, activation='relu', padding='same'))
    model.add(layers.MaxPooling1D(pool_size=2))

    # 移除第三层的池化层，防止数据变得太小
    model.add(layers.Conv1D(256, kernel_size=3, activation='relu', padding='same'))

    # 全连接层
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))

    # 输出层
    model.add(layers.Dense(1, activation='linear'))  # 输出一个值，匹配Y的维度
    return model

# 4. 构建并编译CNN模型
cnn_model = build_cnn((X_train.shape[1], 1))  # 输入形状为(X_train的列数, 1)

# 打印模型结构
print("CNN 模型结构：")
cnn_model.summary()  # 打印CNN模型结构

# 编译模型
cnn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

# 5. 训练模型
history_cnn = cnn_model.fit(
    X_train, Y_train,  # 训练数据和标签
    validation_data=(X_test, Y_test),  # 验证数据和标签
    epochs=100,  # 训练100个轮次
    batch_size=32,  # 批次大小为32
    verbose=1  # 输出详细训练信息
)

# 6. 模型评估与预测
Y_train_pred = cnn_model.predict(X_train).flatten()  # 训练集预测，并将预测结果展平成1D
Y_test_pred = cnn_model.predict(X_test).flatten()  # 测试集预测，并将预测结果展平成1D

# 7. 定义模型评价函数
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    mse = mean_squared_error(Y_true, Y_pred)  # 计算均方误差
    mae = mean_absolute_error(Y_true, Y_pred)  # 计算平均绝对误差
    r2 = r2_score(Y_true, Y_pred)  # 计算R²得分
    evs = explained_variance_score(Y_true, Y_pred)  # 计算解释方差得分
    print(f"{dataset_type} - MSE: {mse:.4f}")
    print(f"{dataset_type} - MAE: {mae:.4f}")
    print(f"{dataset_type} - R²: {r2:.4f}")
    print(f"{dataset_type} - EVS: {evs:.4f}\n")

# 评估训练集和测试集的性能
print("CNN 模型评价指标：")
evaluate_model(Y_train, Y_train_pred, "训练集")  # 评估训练集
evaluate_model(Y_test, Y_test_pred, "测试集")  # 评估测试集

# 8. 绘制训练过程中损失和评价指标的变化
plt.figure(figsize=(10, 6))
plt.plot(history_cnn.history['loss'], label='训练集损失', color='blue')
plt.plot(history_cnn.history['val_loss'], label='验证集损失', color='red')
plt.title('训练和验证损失')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 9. 可视化训练集和测试集的预测值 vs. 真实值
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
