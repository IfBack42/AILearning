# 导入必要的库
import pandas as pd  # 用于数据处理的pandas库
import numpy as np  # 用于数值计算的numpy库
import tensorflow as tf  # 用于深度学习的TensorFlow库
from tensorflow.keras import layers, Model  # 从Keras中导入层和模型模块
from sklearn.model_selection import train_test_split  # 导入数据集划分工具
from sklearn.preprocessing import StandardScaler  # 导入数据标准化工具
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score  # 导入评价指标
import matplotlib.pyplot as plt  # 导入matplotlib库，用于结果的可视化
import warnings  # 警告处理库

# 忽略警告信息
warnings.filterwarnings('ignore')  # 忽略不必要的警告

# 确保使用的是 TensorFlow 2.x
assert tf.__version__.startswith('2'), "请确保使用 TensorFlow 2.x 版本。"  # 确保TensorFlow的版本为2.x

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 设置数据路径，确保路径正确
data = pd.read_excel(data_path)  # 读取Excel文件中的数据

# 2. 数据预处理
# 将最后一列作为目标变量 Y，其余列作为特征 X
X = data.iloc[:, :-1].values  # 选择除最后一列外的所有列作为输入特征
Y = data.iloc[:, -1].values   # 选择最后一列作为输出（目标变量）

# 对特征进行标准化
scaler = StandardScaler()  # 创建一个标准化的对象
X_scaled = scaler.fit_transform(X)  # 对输入特征进行标准化，使其均值为0，方差为1

# 将数据扩展为 3D 形状，以符合LSTM网络的输入要求
X_scaled = np.expand_dims(X_scaled, axis=2)  # 扩展数据的维度，将其从2D变为3D，以适应LSTM输入格式

print(f"特征维度: {X_scaled.shape[1]}")  # 输出特征维度，验证输入数据的形状
print(f"目标变量样本数: {Y.shape[0]}")   # 输出目标变量的样本数，验证输出数据的形状

# 3. 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.2, random_state=42
)  # 将数据集划分为训练集和测试集，80%用于训练，20%用于测试

# 4. 定义双向LSTM网络
def build_bidirectional_lstm(input_shape):  # 定义双向LSTM网络的构建函数
    inputs = layers.Input(shape=input_shape)  # 定义输入层，输入形状为3D
    # 双向LSTM层，第一个LSTM层有128个单元，双向传播
    x = layers.Bidirectional(layers.LSTM(128, activation='tanh', return_sequences=True))(inputs)
    # 第二个双向LSTM层，有64个单元
    x = layers.Bidirectional(layers.LSTM(64, activation='tanh', return_sequences=False))(x)
    # 全连接层，使用64个神经元
    x = layers.Dense(64, activation='relu')(x)
    # 添加Dropout层，防止过拟合
    x = layers.Dropout(0.3)(x)
    # 输出层，线性激活，用于回归
    outputs = layers.Dense(1, activation='linear')(x)
    # 构建模型
    model = Model(inputs=inputs, outputs=outputs)
    return model  # 返回构建的模型

# 5. 定义模型
bilstm_model = build_bidirectional_lstm(input_shape=(X_scaled.shape[1], 1))  # 创建双向LSTM网络模型
bilstm_model.summary()  # 打印模型结构

# 6. 编译模型
bilstm_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])  # 编译模型，使用Adam优化器，损失函数为MSE

# 7. 训练双向LSTM网络
history_bilstm = bilstm_model.fit(
    X_train, Y_train,  # 训练数据和标签
    validation_data=(X_test, Y_test),  # 验证数据和标签
    epochs=1000,  # 训练100个轮次
    batch_size=32,  # 批次大小为32
    verbose=1  # 输出详细训练信息
)

# 8. 模型评估
# 进行预测
Y_train_pred = bilstm_model.predict(X_train).flatten()  # 训练集预测，并将预测结果展平成1D
Y_test_pred = bilstm_model.predict(X_test).flatten()  # 测试集预测，并将预测结果展平成1D

# 定义模型评价函数
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):  # 输入真实值和预测值，计算模型性能
    mse = mean_squared_error(Y_true, Y_pred)  # 计算均方误差
    mae = mean_absolute_error(Y_true, Y_pred)  # 计算平均绝对误差
    r2 = r2_score(Y_true, Y_pred)  # 计算R²得分
    evs = explained_variance_score(Y_true, Y_pred)  # 计算解释方差得分
    print(f"{dataset_type} - MSE: {mse:.4f}")  # 打印MSE
    print(f"{dataset_type} - MAE: {mae:.4f}")  # 打印MAE
    print(f"{dataset_type} - R²: {r2:.4f}")  # 打印R²得分
    print(f"{dataset_type} - EVS: {evs:.4f}\n")  # 打印EVS

# 评估训练集和测试集的性能
print("双向LSTM模型评价指标：")
evaluate_model(Y_train, Y_train_pred, "训练集")  # 评估训练集
evaluate_model(Y_test, Y_test_pred, "测试集")  # 评估测试集

# 9. 结果可视化
plt.figure(figsize=(14, 6))  # 创建画布，设置大小

# 训练集对比图
plt.subplot(1, 2, 1)  # 创建子图
plt.scatter(Y_train, Y_train_pred, color='blue', alpha=0.5, label='预测值')  # 绘制训练集真实值与预测值的散点图
plt.plot([Y_train.min(), Y_train.max()], [Y_train.min(), Y_train.max()], 'k--', lw=2, label='理想情况')  # 绘制理想的参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('训练集: 预测值 vs. 真实值')  # 设置标题
plt.legend()  # 显示图例

# 测试集对比图
plt.subplot(1, 2, 2)  # 创建第二个子图
plt.scatter(Y_test, Y_test_pred, color='green', alpha=0.5, label='预测值')  # 绘制测试集真实值与预测值的散点图
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2, label='理想情况')  # 绘制理想的参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('测试集: 预测值 vs. 真实值')  # 设置标题
plt.legend()  # 显示图例

plt.tight_layout()  # 自动调整子图间的布局，避免重叠
plt.show()  # 显示图像
