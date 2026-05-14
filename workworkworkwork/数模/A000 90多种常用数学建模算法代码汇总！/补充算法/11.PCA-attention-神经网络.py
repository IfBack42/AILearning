import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input, Dense, Dropout, Layer
from tensorflow.keras.models import Model
import tensorflow as tf
from tensorflow.keras import backend as K

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'
data = pd.read_excel(data_path)

# 假设数据的最后一列是输出，前几列是输入
X = data.iloc[:, :-1].values  # 输入特征（前几列）
y = data.iloc[:, -1].values  # 输出标签（最后一列）

# 2. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. PCA降维 (保留 95% 的信息)
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)


# 4. Attention 机制的实现
class Attention(Layer):
    def __init__(self, **kwargs):
        super(Attention, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name='attention_weight',
                                 shape=(input_shape[-1], 1),
                                 initializer='glorot_uniform',
                                 trainable=True)
        self.b = self.add_weight(name='attention_bias',
                                 shape=(input_shape[-1],),
                                 initializer='zeros',
                                 trainable=True)
        super(Attention, self).build(input_shape)

    def call(self, x):
        # 计算注意力权重
        e = K.tanh(K.dot(x, self.W) + self.b)
        alpha = K.softmax(e, axis=1)
        # 输出加权后的特征
        output = x * alpha
        return output


# 5. 构建组合模型
def build_model(input_dim):
    inputs = Input(shape=(input_dim,))

    # Attention 机制
    attention_output = Attention()(inputs)

    # 神经网络部分
    x = Dense(64, activation='relu')(attention_output)
    x = Dropout(0.5)(x)
    x = Dense(32, activation='relu')(x)
    outputs = Dense(1)(x)

    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    return model


# 6. 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

# 7. 构建模型
model = build_model(X_pca.shape[1])

# 8. 训练模型
history = model.fit(X_train, y_train, epochs=500, batch_size=32, validation_data=(X_test, y_test))

# 9. 评估模型
loss, mae = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.4f}, Test MAE: {mae:.4f}")
