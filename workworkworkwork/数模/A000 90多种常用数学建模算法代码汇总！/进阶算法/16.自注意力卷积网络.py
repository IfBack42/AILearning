# 导入必要的库
import numpy as np  # 用于数值计算的库
import pandas as pd  # 用于数据处理的库
import tensorflow as tf  # 用于构建深度学习模型的库
from tensorflow.keras import layers, Model  # 从Keras中导入层和模型模块
from sklearn.preprocessing import StandardScaler  # 用于数据标准化的库
from sklearn.model_selection import train_test_split  # 用于划分数据集
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score  # 用于模型性能评估的指标
import matplotlib.pyplot as plt  # 用于绘制图形的库

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 数据文件路径
data = pd.read_excel(data_path)  # 读取Excel文件中的数据

# 2. 数据预处理
X = data.iloc[:, :-1].values  # 选择除最后一列外的所有列作为输入特征
Y = data.iloc[:, -1].values  # 选择最后一列作为输出（目标变量）

# 数据标准化
scaler = StandardScaler()  # 创建一个标准化对象
X_scaled = scaler.fit_transform(X)  # 对特征进行标准化

# 将数据扩展为3D形式以适应卷积层输入 (samples, timesteps, features)
X_scaled = np.expand_dims(X_scaled, axis=2)  # 扩展数据的维度，增加一维作为特征轴

# 划分训练集和测试集 (80%训练，20%测试)
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)  # 随机划分数据集

# 3. 定义自注意力模块
class SelfAttention(layers.Layer):  # 自定义自注意力模块类，继承Keras的Layer类
    def __init__(self, attention_size):
        super(SelfAttention, self).__init__()  # 调用父类的构造函数
        self.attention_size = attention_size  # 设置注意力的输出维度大小

    def build(self, input_shape):
        # 定义查询 (Q)、键 (K)、值 (V) 的线性变换矩阵
        self.Wq = layers.Dense(self.attention_size)  # 查询矩阵 (Wq)
        self.Wk = layers.Dense(self.attention_size)  # 键矩阵 (Wk)
        self.Wv = layers.Dense(self.attention_size)  # 值矩阵 (Wv)

    def call(self, inputs):
        Q = self.Wq(inputs)  # 对输入计算查询矩阵 Q
        K = self.Wk(inputs)  # 对输入计算键矩阵 K
        V = self.Wv(inputs)  # 对输入计算值矩阵 V

        # 计算缩放点积注意力
        attention_scores = tf.matmul(Q, K, transpose_b=True) / tf.sqrt(tf.cast(self.attention_size, tf.float32))  # 计算 Q 和 K 的缩放点积
        attention_weights = tf.nn.softmax(attention_scores, axis=-1)  # 对注意力分数进行 softmax 操作，得到权重
        attention_output = tf.matmul(attention_weights, V)  # 将权重与值矩阵 V 相乘，得到注意力输出
        return attention_output  # 返回自注意力的输出

# 4. 构建自注意力卷积网络 (SACNN)
def build_sacnn(input_shape):
    inputs = layers.Input(shape=input_shape)  # 定义输入层，输入的形状为 (timesteps, features)

    # 第一层卷积 + 最大池化
    x = layers.Conv1D(64, kernel_size=3, activation='relu', padding='same')(inputs)  # 卷积层，使用ReLU激活函数，核大小为3
    x = layers.MaxPooling1D(pool_size=2)(x)  # 最大池化层，池化窗口大小为2

    # 第二层卷积 + 自注意力模块
    x = layers.Conv1D(128, kernel_size=3, activation='relu', padding='same')(x)  # 第二个卷积层，输出128个特征图
    attention = SelfAttention(attention_size=128)(x)  # 应用自定义的自注意力模块，注意力维度为128

    # 将卷积层的输出和自注意力模块的输出合并
    x = layers.Add()([x, attention])  # 利用加法层将两个张量相加，实现融合

    # 第三层卷积 + 最大池化
    x = layers.Conv1D(256, kernel_size=3, activation='relu', padding='same')(x)  # 第三个卷积层，输出256个特征图
    x = layers.MaxPooling1D(pool_size=2)(x)  # 最大池化层，池化窗口大小为2

    # 全局平均池化层，将每个特征图的值平均化
    x = layers.GlobalAveragePooling1D()(x)

    # 全连接层 + Dropout层
    x = layers.Dense(64, activation='relu')(x)  # 全连接层，输出维度为64
    x = layers.Dropout(0.5)(x)  # Dropout层，防止过拟合，丢弃50%的神经元

    # 输出层，线性激活函数，用于回归问题的预测
    outputs = layers.Dense(1, activation='linear')(x)

    # 构建模型并返回
    model = Model(inputs, outputs)
    return model

# 5. 构建模型
input_shape = (X_train.shape[1], X_train.shape[2])  # 输入形状，包含时间步长和特征数
sacnn_model = build_sacnn(input_shape)  # 构建自注意力卷积网络模型

# 打印模型结构
sacnn_model.summary()  # 输出模型结构信息

# 6. 编译模型
sacnn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])  # 使用Adam优化器，均方误差作为损失函数，MAE作为评价指标

# 7. 训练模型
history_sacnn = sacnn_model.fit(
    X_train, Y_train,  # 输入训练数据和目标值
    validation_data=(X_test, Y_test),  # 验证集数据
    epochs=500,  # 训练的轮次
    batch_size=32,  # 每批次数据量
    verbose=1  # 输出详细训练信息
)

# 8. 模型评估与预测
Y_train_pred = sacnn_model.predict(X_train).flatten()  # 对训练集进行预测，并将输出展平成一维
Y_test_pred = sacnn_model.predict(X_test).flatten()  # 对测试集进行预测，并将输出展平成一维

# 定义模型性能评价函数
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    mse = mean_squared_error(Y_true, Y_pred)  # 计算均方误差
    mae = mean_absolute_error(Y_true, Y_pred)  # 计算平均绝对误差
    r2 = r2_score(Y_true, Y_pred)  # 计算R²得分
    evs = explained_variance_score(Y_true, Y_pred)  # 计算解释方差得分
    print(f"{dataset_type} - MSE: {mse:.4f}")  # 打印MSE
    print(f"{dataset_type} - MAE: {mae:.4f}")  # 打印MAE
    print(f"{dataset_type} - R²: {r2:.4f}")  # 打印R²
    print(f"{dataset_type} - EVS: {evs:.4f}\n")  # 打印EVS

# 评估训练集和测试集的性能
evaluate_model(Y_train, Y_train_pred, "训练集")  # 评估训练集
evaluate_model(Y_test, Y_test_pred, "测试集")  # 评估测试集

# 9. 绘制损失变化曲线
plt.figure(figsize=(10, 6))  # 创建图形窗口
plt.plot(history_sacnn.history['loss'], label='Train Loss', color='blue')  # 绘制训练损失曲线
plt.plot(history_sacnn.history['val_loss'], label='Validation Loss', color='red')  # 绘制验证损失曲线
plt.title('Training and Validation Loss')  # 图像标题
plt.xlabel('Epochs')  # X轴标签
plt.ylabel('Loss')  # Y轴标签
plt.legend()  # 显示图例
plt.grid(True)  # 显示网格
plt.tight_layout()  # 自动调整布局
plt.show()  # 显示图像

# 10. 可视化训练集和测试集的预测值 vs. 真实值
plt.figure(figsize=(14, 6))  # 创建画布，设置图形大小

# 训练集对比图
plt.subplot(1, 2, 1)  # 创建第一个子图
plt.scatter(Y_train, Y_train_pred, color='blue', alpha=0.5, label='预测值')  # 绘制训练集的真实值与预测值的散点图
plt.plot([Y_train.min(), Y_train.max()], [Y_train.min(), Y_train.max()], 'k--', lw=2, label='理想情况')  # 绘制理想情况下的参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('训练集: 预测值 vs. 真实值')  # 设置图形标题
plt.legend()  # 显示图例

# 测试集对比图
plt.subplot(1, 2, 2)  # 创建第二个子图
plt.scatter(Y_test, Y_test_pred, color='green', alpha=0.5, label='预测值')  # 绘制测试集的真实值与预测值的散点图
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2, label='理想情况')  # 绘制理想情况下的参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('测试集: 预测值 vs. 真实值')  # 设置图形标题
plt.legend()  # 显示图例

plt.tight_layout()  # 自动调整布局，防止子图重叠
plt.show()  # 显示图像
