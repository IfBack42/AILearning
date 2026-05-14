# 导入必要的库
import numpy as np  # 用于数值计算
import pandas as pd  # 用于数据处理
import tensorflow as tf  # 深度学习库
from tensorflow.keras import layers, Model  # 导入Keras的层和模型模块
from sklearn.preprocessing import StandardScaler  # 数据标准化
from sklearn.model_selection import train_test_split  # 数据集划分
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score  # 模型评估指标
import matplotlib.pyplot as plt  # 绘图库

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 设置数据路径
data = pd.read_excel(data_path)  # 读取Excel文件数据

# 2. 数据预处理
X = data.iloc[:, :-1].values  # 输入特征（去除最后一列）
Y = data.iloc[:, -1].values  # 输出目标变量（最后一列）

# 数据标准化
scaler = StandardScaler()  # 创建标准化对象
X_scaled = scaler.fit_transform(X)  # 标准化特征

# 扩展数据维度以适应时空注意网络的输入 (samples, timesteps, features)
X_scaled = np.expand_dims(X_scaled, axis=2)  # 增加一个维度，形成3D输入

# 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)  # 80%训练，20%测试

# 3. 定义时空注意模块
class TemporalAttention(layers.Layer):
    """
    时序注意力模块，关注数据随时间变化的动态。
    """
    def __init__(self, attention_size):
        super(TemporalAttention, self).__init__()
        self.attention_size = attention_size  # 定义注意力的输出维度

    def build(self, input_shape):
        # 定义时间维度的查询（Q）、键（K）和值（V）的线性变换矩阵
        self.Wq = layers.Dense(self.attention_size)  # 查询矩阵
        self.Wk = layers.Dense(self.attention_size)  # 键矩阵
        self.Wv = layers.Dense(self.attention_size)  # 值矩阵

    def call(self, inputs):
        # 计算查询、键、值矩阵
        Q = self.Wq(inputs)  # 查询矩阵
        K = self.Wk(inputs)  # 键矩阵
        V = self.Wv(inputs)  # 值矩阵

        # 计算缩放点积注意力
        attention_scores = tf.matmul(Q, K, transpose_b=True) / tf.sqrt(tf.cast(self.attention_size, tf.float32))  # 缩放点积
        attention_weights = tf.nn.softmax(attention_scores, axis=-1)  # softmax得到注意力权重
        attention_output = tf.matmul(attention_weights, V)  # 计算注意力输出

        return attention_output  # 返回时序注意力的输出

class SpatialAttention(layers.Layer):
    """
    空间注意力模块，关注特征的空间相关性。
    """
    def __init__(self, attention_size):
        super(SpatialAttention, self).__init__()
        self.attention_size = attention_size  # 定义注意力的输出维度

    def build(self, input_shape):
        # 定义空间维度的查询（Q）、键（K）和值（V）的线性变换矩阵
        self.Wq = layers.Dense(self.attention_size)  # 查询矩阵
        self.Wk = layers.Dense(self.attention_size)  # 键矩阵
        self.Wv = layers.Dense(self.attention_size)  # 值矩阵

    def call(self, inputs):
        # 计算查询、键、值矩阵
        Q = self.Wq(inputs)  # 查询矩阵
        K = self.Wk(inputs)  # 键矩阵
        V = self.Wv(inputs)  # 值矩阵

        # 计算缩放点积注意力
        attention_scores = tf.matmul(Q, K, transpose_b=True) / tf.sqrt(tf.cast(self.attention_size, tf.float32))  # 缩放点积
        attention_weights = tf.nn.softmax(attention_scores, axis=-1)  # softmax得到注意力权重
        attention_output = tf.matmul(attention_weights, V)  # 计算注意力输出

        return attention_output  # 返回空间注意力的输出

# 4. 构建时空注意卷积网络 (STAN)
def build_stan(input_shape):
    inputs = layers.Input(shape=input_shape)  # 输入层

    # 第一层卷积 + 最大池化
    x = layers.Conv1D(64, kernel_size=3, activation='relu', padding='same')(inputs)  # 卷积层
    x = layers.MaxPooling1D(pool_size=2)(x)  # 最大池化层

    # 第二层卷积
    x = layers.Conv1D(128, kernel_size=3, activation='relu', padding='same')(x)  # 卷积层

    # 时序注意力模块
    temporal_attention = TemporalAttention(attention_size=128)(x)  # 时序注意力模块

    # 空间注意力模块
    spatial_attention = SpatialAttention(attention_size=128)(x)  # 空间注意力模块

    # 将时序和空间注意力模块的输出与卷积输出相加，融合信息
    x = layers.Add()([x, temporal_attention, spatial_attention])  # 融合输出

    # 第三层卷积 + 最大池化
    x = layers.Conv1D(256, kernel_size=3, activation='relu', padding='same')(x)  # 卷积层
    x = layers.MaxPooling1D(pool_size=2)(x)  # 最大池化层

    # 全局平均池化
    x = layers.GlobalAveragePooling1D()(x)  # 全局平均池化层

    # 全连接层 + Dropout
    x = layers.Dense(64, activation='relu')(x)  # 全连接层
    x = layers.Dropout(0.5)(x)  # Dropout层，防止过拟合

    # 输出层（线性激活函数，用于回归任务）
    outputs = layers.Dense(1, activation='linear')(x)  # 输出层

    # 构建模型
    model = Model(inputs, outputs)
    return model  # 返回构建好的模型

# 5. 构建时空注意卷积网络模型
input_shape = (X_train.shape[1], X_train.shape[2])  # 输入形状
stan_model = build_stan(input_shape)  # 构建STAN模型

# 打印模型结构
stan_model.summary()  # 输出模型结构信息

# 6. 编译模型
stan_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])  # 使用Adam优化器，均方误差作为损失函数，MAE作为指标

# 7. 训练模型
history_stan = stan_model.fit(
    X_train, Y_train,  # 输入训练数据和标签
    validation_data=(X_test, Y_test),  # 验证数据
    epochs=100,  # 训练轮次
    batch_size=32,  # 批次大小
    verbose=1  # 输出详细训练信息
)

# 8. 评估模型性能
Y_train_pred = stan_model.predict(X_train).flatten()  # 预测训练集，并展平成1D
Y_test_pred = stan_model.predict(X_test).flatten()  # 预测测试集，并展平成1D

# 定义模型评估函数
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    mse = mean_squared_error(Y_true, Y_pred)  # 均方误差
    mae = mean_absolute_error(Y_true, Y_pred)  # 平均绝对误差
    r2 = r2_score(Y_true, Y_pred)  # R²得分
    evs = explained_variance_score(Y_true, Y_pred)  # 解释方差得分
    print(f"{dataset_type} - MSE: {mse:.4f}")
    print(f"{dataset_type} - MAE: {mae:.4f}")
    print(f"{dataset_type} - R²: {r2:.4f}")
    print(f"{dataset_type} - EVS: {evs:.4f}\n")

# 评估训练集和测试集的性能
evaluate_model(Y_train, Y_train_pred, "训练集")
evaluate_model(Y_test, Y_test_pred, "测试集")

# 9. 绘制损失变化曲线
plt.figure(figsize=(10, 6))  # 创建画布，设置大小
plt.plot(history_stan.history['loss'], label='训练损失', color='blue')  # 绘制训练损失
plt.plot(history_stan.history['val_loss'], label='验证损失', color='red')  # 绘制验证损失
plt.title('训练和验证损失')  # 设置标题
plt.xlabel('Epochs')  # 设置x轴标签
plt.ylabel('Loss')  # 设置y轴标签
plt.legend()  # 显示图例
plt.grid(True)  # 显示网格线
plt.tight_layout()  # 自动调整布局
plt.show()  # 显示图形

# 10. 可视化训练集和测试集的预测值 vs. 真实值
plt.figure(figsize=(14, 6))  # 创建一个新的画布

# 训练集对比图
plt.subplot(1, 2, 1)  # 创建第一个子图
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

plt.tight_layout()  # 自动调整子图间的布局，防止重叠
plt.show()  # 显示图形
