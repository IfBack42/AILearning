# 导入必要的库
import numpy as np
import pandas as pd
import tensorflow as tf  # 用于神经网络的TensorFlow库
from tensorflow.keras import layers, Model  # 用于模型的Keras库
from sklearn.preprocessing import StandardScaler  # 用于特征标准化的工具
from sklearn.model_selection import train_test_split  # 用于划分训练集和测试集的工具
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score  # 用于模型评价的指标
import matplotlib.pyplot as plt  # 用于可视化的工具

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 设置数据路径
data = pd.read_excel(data_path)  # 读取Excel文件中的数据

# 2. 数据预处理
# 将最后一列作为目标变量Y，其他列作为特征X
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values  # 输出目标变量

# 标准化特征数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 将数据划分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)


# 3. 构建KAN神经网络的基本组件
# 在KAN网络中，通常包含若干个注意力模块和特征组合机制

# 定义KAN注意力模块
class KanAttentionLayer(layers.Layer):
    def __init__(self, units):
        super(KanAttentionLayer, self).__init__()
        self.units = units  # 设置单元数量

        # 定义线性变换层
        self.wq = layers.Dense(units)  # 查询权重层
        self.wk = layers.Dense(units)  # 键权重层
        self.wv = layers.Dense(units)  # 值权重层
        self.fc = layers.Dense(units)  # 输出全连接层

    def call(self, inputs):
        # 线性变换查询、键和值
        q = self.wq(inputs)  # 查询Q
        k = self.wk(inputs)  # 键K
        v = self.wv(inputs)  # 值V

        # 计算注意力分数
        attn_score = tf.matmul(q, k, transpose_b=True)
        attn_weights = tf.nn.softmax(attn_score, axis=-1)  # 通过softmax获得注意力权重

        # 使用注意力权重加权平均
        attn_output = tf.matmul(attn_weights, v)
        return self.fc(attn_output)  # 通过全连接层输出


# 定义KAN模型结构
def build_kan(input_shape, units, output_dim):
    inputs = layers.Input(shape=input_shape)  # 定义输入层
    x = layers.Dense(units, activation='relu')(inputs)  # 首先经过全连接层

    # 添加KAN注意力模块
    attention_output = KanAttentionLayer(units)(x)

    # 全连接层进行输出
    x = layers.Dense(units, activation='relu')(attention_output)
    outputs = layers.Dense(output_dim, activation='linear')(x)  # 输出层，线性激活函数

    # 构建KAN模型
    model = Model(inputs=inputs, outputs=outputs)
    return model


# 4. 构建和编译KAN模型
kan_model = build_kan(input_shape=(X_train.shape[1],), units=64, output_dim=1)  # 构建KAN模型
kan_model.summary()  # 打印KAN模型的结构

kan_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])  # 编译模型

# 5. 训练KAN模型
history_kan = kan_model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=200, batch_size=32, verbose=1)

# 6. 评估模型性能并进行预测
Y_train_pred = kan_model.predict(X_train).flatten()  # 训练集的预测值
Y_test_pred = kan_model.predict(X_test).flatten()  # 测试集的预测值


# 定义模型评价函数
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
print("KAN模型评价指标：")
evaluate_model(Y_train, Y_train_pred, "训练集")
evaluate_model(Y_test, Y_test_pred, "测试集")

# 7. 绘制训练过程中损失的变化
plt.figure(figsize=(10, 6))  # 创建画布，设置大小
plt.plot(history_kan.history['loss'], label='训练损失', color='blue')  # 绘制训练损失曲线
plt.plot(history_kan.history['val_loss'], label='验证损失', color='red')  # 绘制验证损失曲线
plt.title('训练和验证损失')  # 设置标题
plt.xlabel('Epochs')  # 设置x轴标签
plt.ylabel('Loss')  # 设置y轴标签
plt.legend()  # 显示图例
plt.grid(True)  # 显示网格线
plt.tight_layout()  # 自动调整布局
plt.show()  # 显示图形

# 8. 可视化训练集和测试集的预测值 vs. 真实值
plt.figure(figsize=(14, 6))  # 创建一个新的画布

# 训练集对比图
plt.subplot(1, 2, 1)  # 创建第一个子图
plt.scatter(Y_train, Y_train_pred, color='blue', alpha=0.5, label='预测值')  # 绘制训练集真实值与预测值的散点图
plt.plot([Y_train.min(), Y_train.max()], [Y_train.min(), Y_train.max()], 'k--', lw=2, label='理想情况')  # 绘制理想参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('训练集: 预测值 vs. 真实值')  # 设置标题
plt.legend()  # 显示图例

# 测试集对比图
plt.subplot(1, 2, 2)  # 创建第二个子图
plt.scatter(Y_test, Y_test_pred, color='green', alpha=0.5, label='预测值')  # 绘制测试集真实值与预测值的散点图
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2, label='理想情况')  # 绘制理想参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('测试集: 预测值 vs. 真实值')  # 设置标题
plt.legend()  # 显示图例

plt.tight_layout()  # 自动调整子图间的布局
plt.show()  # 显示图形
