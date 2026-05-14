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

# 将数据扩展为 3D 形状，以符合Transformer模型的输入要求
X_scaled = np.expand_dims(X_scaled, axis=2)  # 扩展数据的维度，将其从2D变为3D，以适应Transformer输入格式

print(f"特征维度: {X_scaled.shape[1]}")  # 输出特征维度，验证输入数据的形状
print(f"目标变量样本数: {Y.shape[0]}")   # 输出目标变量的样本数，验证输出数据的形状

# 3. 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.2, random_state=42
)  # 将数据集划分为训练集和测试集，80%用于训练，20%用于测试

# 4. 定义Transformer模型的基本组件

# 位置编码函数：用于添加位置信息，使Transformer模型能够感知序列的位置信息
def positional_encoding(seq_len, d_model):
    # 初始化位置编码矩阵
    pos_encoding = np.zeros((seq_len, d_model))
    for pos in range(seq_len):  # 遍历每个位置
        for i in range(0, d_model, 2):  # 偶数维度位置使用sin函数
            pos_encoding[pos, i] = np.sin(pos / (10000 ** (i / d_model)))
        for i in range(1, d_model, 2):  # 奇数维度位置使用cos函数
            pos_encoding[pos, i] = np.cos(pos / (10000 ** (i / d_model)))
    return tf.cast(pos_encoding, dtype=tf.float32)  # 将位置编码矩阵转化为Tensor

# 多头注意力机制的实现
class MultiHeadAttention(layers.Layer):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0  # 确保模型维度可以被头的数量整除
        self.d_model = d_model  # 模型的总维度
        self.num_heads = num_heads  # 注意力头的数量
        self.depth = d_model // num_heads  # 每个注意力头的维度

        # 定义线性变换矩阵，用于Q（查询），K（键）和V（值）
        self.wq = layers.Dense(d_model)
        self.wk = layers.Dense(d_model)
        self.wv = layers.Dense(d_model)
        self.dense = layers.Dense(d_model)  # 最终的线性层，用于输出拼接后的多头注意力

    def split_heads(self, x, batch_size):
        # 将最后一维切分为 (num_heads, depth)，然后调整维度为(batch_size, num_heads, seq_len, depth)
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
        return tf.transpose(x, perm=[0, 2, 1, 3])  # 交换维度，使头维度在前

    def call(self, v, k, q):
        batch_size = tf.shape(q)[0]  # 获取批次大小

        # 线性变换查询、键、值
        q = self.wq(q)  # 计算查询Q
        k = self.wk(k)  # 计算键K
        v = self.wv(v)  # 计算值V

        # 将Q、K、V拆分为多个头
        q = self.split_heads(q, batch_size)
        k = self.split_heads(k, batch_size)
        v = self.split_heads(v, batch_size)

        # 计算缩放点积注意力
        scaled_attention, attention_weights = scaled_dot_product_attention(q, k, v)
        # 将多个头的输出拼接在一起
        scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])
        concat_attention = tf.reshape(scaled_attention, (batch_size, -1, self.d_model))

        # 通过线性层
        output = self.dense(concat_attention)
        return output

# 缩放点积注意力机制
def scaled_dot_product_attention(q, k, v):
    matmul_qk = tf.matmul(q, k, transpose_b=True)  # 计算Q和K的点积

    # 缩放点积
    dk = tf.cast(tf.shape(k)[-1], tf.float32)
    scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)

    # 应用softmax得到注意力权重
    attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)

    # 计算最终的注意力输出
    output = tf.matmul(attention_weights, v)
    return output, attention_weights

# 定义Transformer编码器层
class TransformerEncoderLayer(layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super(TransformerEncoderLayer, self).__init__()
        self.mha = MultiHeadAttention(d_model, num_heads)  # 多头注意力机制
        self.ffn = tf.keras.Sequential([
            layers.Dense(dff, activation='relu'),  # 前馈网络第一层
            layers.Dense(d_model)  # 前馈网络第二层
        ])
        # Layer Normalization
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        # Dropout层
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, x, training):  # 添加 training 参数，确保 Dropout 和 LayerNorm 在训练和推理中表现不同
        # 计算自注意力
        attn_output = self.mha(x, x, x)  # 多头自注意力
        attn_output = self.dropout1(attn_output, training=training)  # 在训练时应用Dropout
        out1 = self.layernorm1(x + attn_output)  # 残差连接 + Layer Normalization

        ffn_output = self.ffn(out1)  # 前馈网络
        ffn_output = self.dropout2(ffn_output, training=training)  # 在训练时应用Dropout
        out2 = self.layernorm2(out1 + ffn_output)  # 残差连接 + Layer Normalization

        return out2

# 5. 定义完整的Transformer网络
def build_transformer(input_shape, num_layers, d_model, num_heads, dff, rate=0.1):
    inputs = layers.Input(shape=input_shape)  # 定义输入层，输入形状为3D
    seq_len = input_shape[0]  # 获取序列长度
    pos_encoding = positional_encoding(seq_len, d_model)  # 计算位置编码

    x = layers.Dense(d_model)(inputs)  # 对输入数据进行线性变换
    x += pos_encoding  # 将位置编码加入到输入数据中

    for _ in range(num_layers):
        x = TransformerEncoderLayer(d_model, num_heads, dff, rate)(x, training=True)  # 多层Transformer编码器，显式传递training参数

    x = layers.GlobalAveragePooling1D()(x)  # 全局平均池化
    x = layers.Dense(64, activation='relu')(x)  # 全连接层
    x = layers.Dropout(rate)(x)  # Dropout层
    outputs = layers.Dense(1, activation='linear')(x)  # 输出层，线性激活函数

    model = Model(inputs=inputs, outputs=outputs)  # 构建模型
    return model

# 6. 定义模型
transformer_model = build_transformer(
    input_shape=(X_scaled.shape[1], 1),  # 输入形状为3D
    num_layers=2,  # Transformer编码器层数
    d_model=128,  # 总维度
    num_heads=8,  # 注意力头数
    dff=512,  # 前馈网络中隐藏层的维度
    rate=0.1  # Dropout比率
)
transformer_model.summary()  # 打印模型结构

# 7. 编译模型
transformer_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])  # 编译模型

# 8. 训练Transformer模型
history_transformer = transformer_model.fit(
    X_train, Y_train,  # 训练数据和标签
    validation_data=(X_test, Y_test),  # 验证数据和标签
    epochs=1000,  # 训练100个轮次
    batch_size=32,  # 批次大小为32
    verbose=1  # 输出详细训练信息
)

# 9. 模型评估与预测
Y_train_pred = transformer_model.predict(X_train).flatten()  # 训练集预测，并将预测结果展平成1D
Y_test_pred = transformer_model.predict(X_test).flatten()  # 测试集预测，并将预测结果展平成1D

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
print("Transformer 模型评价指标：")
evaluate_model(Y_train, Y_train_pred, "训练集")  # 评估训练集
evaluate_model(Y_test, Y_test_pred, "测试集")  # 评估测试集

# 10. 结果可视化
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
