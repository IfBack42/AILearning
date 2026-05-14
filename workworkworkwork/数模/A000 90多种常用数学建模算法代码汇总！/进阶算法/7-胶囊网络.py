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

# 将数据扩展为3D，适应Conv1D层的输入格式
X_scaled = np.expand_dims(X_scaled, axis=-1)  # 扩展为 [样本数, 时间步, 特征数]

# 将数据划分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

# 3. 定义胶囊层
class CapsuleLayer(layers.Layer):
    def __init__(self, num_capsules, dim_capsules, routings=3, **kwargs):
        super(CapsuleLayer, self).__init__(**kwargs)
        self.num_capsules = num_capsules  # 定义胶囊的数量
        self.dim_capsules = dim_capsules  # 每个胶囊的维度
        self.routings = routings  # 路由次数

    def build(self, input_shape):
        self.input_num_capsules = input_shape[1]
        self.input_dim_capsules = input_shape[2]

        # 定义权重矩阵
        self.W = self.add_weight(shape=[self.input_num_capsules, self.num_capsules, self.input_dim_capsules, self.dim_capsules],
                                 initializer='glorot_uniform', trainable=True)

    def call(self, inputs):
        # 扩展输入数据的维度，用于与权重矩阵相乘
        inputs_expand = tf.expand_dims(inputs, 2)  # [batch_size, input_num_capsules, 1, input_dim_capsules]
        inputs_tiled = tf.tile(inputs_expand, [1, 1, self.num_capsules, 1])  # [batch_size, input_num_capsules, num_capsules, input_dim_capsules]
        inputs_tiled = tf.expand_dims(inputs_tiled, -1)  # [batch_size, input_num_capsules, num_capsules, input_dim_capsules, 1]

        # 扩展权重矩阵的维度
        W_tiled = tf.tile(tf.expand_dims(self.W, 0), [tf.shape(inputs)[0], 1, 1, 1, 1])  # [batch_size, input_num_capsules, num_capsules, input_dim_capsules, dim_capsules]

        # 计算"预测向量" u_hat
        u_hat = tf.matmul(W_tiled, inputs_tiled)  # [batch_size, input_num_capsules, num_capsules, dim_capsules, 1]
        u_hat = tf.squeeze(u_hat, -1)  # [batch_size, input_num_capsules, num_capsules, dim_capsules]

        # 路由算法的初始化
        b = tf.zeros(shape=[tf.shape(inputs)[0], self.input_num_capsules, self.num_capsules])

        # 动态路由算法
        for i in range(self.routings):
            c = tf.nn.softmax(b, axis=2)  # [batch_size, input_num_capsules, num_capsules]
            c_expanded = tf.expand_dims(c, -1)  # [batch_size, input_num_capsules, num_capsules, 1]
            s = tf.reduce_sum(c_expanded * u_hat, axis=1)  # [batch_size, num_capsules, dim_capsules]
            v = self.squash(s)  # [batch_size, num_capsules, dim_capsules]

            if i < self.routings - 1:
                v_expanded = tf.expand_dims(v, 1)  # [batch_size, 1, num_capsules, dim_capsules]
                u_v_product = tf.reduce_sum(u_hat * v_expanded, axis=-1)  # [batch_size, input_num_capsules, num_capsules]
                b += u_v_product

        return v  # [batch_size, num_capsules, dim_capsules]

    @staticmethod
    def squash(vectors, axis=-1):
        # 定义squash函数，将输入压缩到长度为1的范围内
        s_squared_norm = tf.reduce_sum(tf.square(vectors), axis=axis, keepdims=True) + tf.keras.backend.epsilon()
        scale = s_squared_norm / (1.0 + s_squared_norm)
        return scale * vectors / tf.sqrt(s_squared_norm)

# 4. 构建胶囊网络模型
def build_capsule_network(input_shape, num_capsules, dim_capsules, routings=3):
    inputs = layers.Input(shape=input_shape)  # 定义输入层

    # 增加卷积层的数量和滤波器数量
    conv1 = layers.Conv1D(128, 3, activation='relu', padding='same')(inputs)
    conv2 = layers.Conv1D(256, 3, strides=1, activation='relu', padding='same')(conv1)
    conv3 = layers.Conv1D(256, 3, strides=2, activation='relu', padding='same')(conv2)
    conv4 = layers.Conv1D(512, 3, strides=1, activation='relu', padding='same')(conv3)

    # 主胶囊层
    primary_caps = layers.Conv1D(512, 3, strides=2, activation='relu', padding='same')(conv4)
    primary_caps = layers.Reshape((-1, 32))(primary_caps)  # 将卷积层输出转换为胶囊

    # 增加胶囊层的胶囊数量和维度
    caps_layer = CapsuleLayer(num_capsules=num_capsules*2, dim_capsules=dim_capsules*2, routings=routings)(primary_caps)

    # 全连接层
    flatten = layers.Flatten()(caps_layer)
    dense1 = layers.Dense(256, activation='relu')(flatten)
    dense2 = layers.Dense(128, activation='relu')(dense1)
    dense3 = layers.Dense(64, activation='relu')(dense2)
    output = layers.Dense(1, activation='linear')(dense3)

    # 构建模型
    model = Model(inputs=inputs, outputs=output)
    return model

# 5. 定义模型参数
input_shape = (X_train.shape[1], X_train.shape[2])  # 输入形状
num_capsules = 10  # 原始胶囊数量
dim_capsules = 16  # 原始每个胶囊的维度

# 6. 构建胶囊网络
capsnet_model = build_capsule_network(input_shape, num_capsules, dim_capsules)

# 打印模型结构
capsnet_model.summary()

# 7. 编译模型
capsnet_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), loss='mse', metrics=['mae'])

# 8. 训练模型（取消早停机制）
history_capsnet = capsnet_model.fit(X_train, Y_train, validation_data=(X_test, Y_test),
                                    epochs=300, batch_size=16, verbose=1)

# 9. 模型评估与预测
Y_train_pred = capsnet_model.predict(X_train).flatten()  # 训练集预测
Y_test_pred = capsnet_model.predict(X_test).flatten()  # 测试集预测

# 定义模型评价函数
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

# 10. 结果可视化
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
