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
scaler = StandardScaler()  # 初始化标准化器
X_scaled = scaler.fit_transform(X)  # 对X进行标准化

# 将数据扩展为3D形状，适应卷积层的输入要求
X_scaled = np.expand_dims(X_scaled, axis=2)

# 3. 构建卷积模块函数
def conv_block(inputs, filters, kernel_size=3, pool_size=1):
    """构建一个卷积模块，包括卷积层、激活层、池化层"""
    x = layers.Conv1D(filters=filters, kernel_size=kernel_size, padding='same', activation='relu')(inputs)
    if x.shape[1] > 1:  # 只有在序列长度大于1时才进行池化操作
        x = layers.MaxPooling1D(pool_size=pool_size)(x)
    return x

# 4. 构建递归卷积神经网络（RCNN）
def build_rcnn_optimized(input_shape, num_filters, num_recurrent_units, output_dim, dropout_rate=0.5):
    """构建优化后的RCNN模型"""
    inputs = layers.Input(shape=input_shape)  # 输入层

    # 卷积层模块
    x = conv_block(inputs, filters=num_filters)  # 第一个卷积模块
    x = conv_block(x, filters=num_filters * 2)  # 第二个卷积模块
    x = conv_block(x, filters=num_filters * 4)  # 第三个卷积模块

    # LSTM层，增加dropout防止过拟合
    x = layers.LSTM(num_recurrent_units, return_sequences=False, dropout=dropout_rate)(x)

    # 输出层（线性激活函数用于回归任务）
    outputs = layers.Dense(output_dim, activation='linear')(x)

    # 构建模型
    model = Model(inputs=inputs, outputs=outputs)
    return model

# 5. 构建并编译优化后的RCNN模型
rcnn_model_optimized = build_rcnn_optimized(
    input_shape=(X_train.shape[1], 1),  # 输入形状为（样本数量，1）
    num_filters=128,  # 第一个卷积层的卷积核数量
    num_recurrent_units=256,  # LSTM层的单元数量
    output_dim=1,  # 输出为1维（回归问题）
    dropout_rate=0.1  # Dropout比率，防止过拟合
)

# 编译模型，使用Adam优化器和均方误差损失函数
rcnn_model_optimized.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), loss='mse', metrics=['mae'])

# 打印模型结构
rcnn_model_optimized.summary()

# 6. 训练模型
history_rcnn_optimized = rcnn_model_optimized.fit(
    X_train, Y_train,  # 训练数据和标签
    validation_data=(X_test, Y_test),  # 验证数据和标签
    epochs=1200,  # 训练1200个轮次
    batch_size=64,  # 批次大小为64
    verbose=1  # 输出详细训练信息
)

# 7. 模型评估与预测
Y_train_pred = rcnn_model_optimized.predict(X_train).flatten()  # 训练集预测
Y_test_pred = rcnn_model_optimized.predict(X_test).flatten()  # 测试集预测

# 8. 计算4个详细的数字评价指标
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

# 9. 绘制训练过程中损失的变化
plt.figure(figsize=(10, 6))
plt.plot(history_rcnn_optimized.history['loss'], label='训练集损失', color='blue')
plt.plot(history_rcnn_optimized.history['val_loss'], label='验证集损失', color='red')
plt.title('RCNN 训练和验证损失')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 10. 可视化训练集和测试集的预测值 vs. 真实值
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
