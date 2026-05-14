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
data = pd.read_excel(data_path)  # 读取Excel文件中的数据

# 2. 数据预处理
# 假设最后一列是目标变量Y，其他列是特征X
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values   # 输出（目标变量）

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 将数据扩展为 3D 形状，适用于 LSTM/QR-CNN
X_scaled = np.expand_dims(X_scaled, axis=2)

# 将数据划分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.2, random_state=42)

# 3. 多头注意力机制
class MultiHeadAttention(layers.Layer):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.depth = d_model // num_heads

        # 定义线性变换矩阵，用于查询(Q)，键(K)和值(V)
        self.wq = layers.Dense(d_model)
        self.wk = layers.Dense(d_model)
        self.wv = layers.Dense(d_model)
        self.dense = layers.Dense(d_model)

    def split_heads(self, x, batch_size):
        # 分割多头，每头的深度是 d_model // num_heads
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
        return tf.transpose(x, perm=[0, 2, 1, 3])

    def call(self, v, k, q):
        batch_size = tf.shape(q)[0]

        # 线性变换
        q = self.wq(q)
        k = self.wk(k)
        v = self.wv(v)

        # 多头分割
        q = self.split_heads(q, batch_size)
        k = self.split_heads(k, batch_size)
        v = self.split_heads(v, batch_size)

        # 计算缩放点积注意力
        scaled_attention, _ = self.scaled_dot_product_attention(q, k, v)

        # 合并头
        scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])
        concat_attention = tf.reshape(scaled_attention, (batch_size, -1, self.num_heads * self.depth))

        output = self.dense(concat_attention)  # 输出线性层
        return output

    def scaled_dot_product_attention(self, q, k, v):
        # 点积
        matmul_qk = tf.matmul(q, k, transpose_b=True)

        # 缩放
        dk = tf.cast(tf.shape(k)[-1], tf.float32)
        scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)

        # softmax 计算权重
        attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)

        # 应用权重到 V
        output = tf.matmul(attention_weights, v)
        return output, attention_weights

# 4. QR-CNN层：使用QR分解进行卷积
class QRCNNLayer(layers.Layer):
    def __init__(self, filters, kernel_size, strides=1):
        super(QRCNNLayer, self).__init__()
        self.conv = layers.Conv1D(filters, kernel_size, strides=strides, padding='same')
        self.qr = layers.Lambda(lambda x: tf.linalg.qr(x)[0])  # QR分解，只提取Q矩阵

    def call(self, inputs):
        x = self.conv(inputs)  # 1D卷积
        x = self.qr(x)  # QR分解
        return x

# 5. 构建复杂的 QRCNN-LSTM-Attention 模型
def build_qrcnn_lstm_attention_model(input_shape, d_model, num_heads):
    inputs = layers.Input(shape=input_shape)

    # 增加QR-CNN层的深度和宽度
    qrcnn = QRCNNLayer(128, 3)(inputs)
    qrcnn = layers.BatchNormalization()(qrcnn)
    qrcnn = layers.Activation('relu')(qrcnn)
    qrcnn = layers.Dropout(0.3)(qrcnn)

    qrcnn = QRCNNLayer(128, 3)(qrcnn)
    qrcnn = layers.BatchNormalization()(qrcnn)
    qrcnn = layers.Activation('relu')(qrcnn)
    qrcnn = layers.Dropout(0.3)(qrcnn)

    # LSTM层
    lstm = layers.LSTM(128, return_sequences=True)(qrcnn)
    lstm = layers.BatchNormalization()(lstm)
    lstm = layers.Dropout(0.3)(lstm)

    # 多头注意力层
    attention = MultiHeadAttention(d_model, num_heads)(lstm, lstm, lstm)
    attention = layers.BatchNormalization()(attention)
    attention = layers.Dropout(0.3)(attention)

    # 全局平均池化层
    global_avg_pool = layers.GlobalAveragePooling1D()(attention)

    # 全连接层
    dense = layers.Dense(128, activation='relu')(global_avg_pool)
    dense = layers.BatchNormalization()(dense)
    dense = layers.Dropout(0.3)(dense)

    outputs = layers.Dense(1, activation='linear')(dense)

    # 构建模型
    model = Model(inputs=inputs, outputs=outputs)
    return model

# 6. 构建并编译模型
input_shape = (X_scaled.shape[1], X_scaled.shape[2])  # 输入形状
d_model = 256  # 总维度，增大为256
num_heads = 8  # 注意力头数
model = build_qrcnn_lstm_attention_model(input_shape, d_model, num_heads)

# 使用 Huber 损失函数和 Adam 优化器，增大学习率
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.005),
              loss=tf.keras.losses.Huber(),
              metrics=['mae'])

# 打印模型结构
model.summary()

# 7. 训练模型（增加训练轮数，减小批次大小）
history = model.fit(X_train, Y_train,
                    epochs=500,
                    batch_size=16,
                    validation_split=0.2,
                    verbose=1)

# 8. 模型评估
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

# 9. 绘制训练过程中的损失曲线
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='训练损失')
plt.plot(history.history['val_loss'], label='验证损失')
plt.title('模型训练过程中的损失曲线')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

# 10. 绘制训练集和测试集的预测值 vs. 真实值
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
