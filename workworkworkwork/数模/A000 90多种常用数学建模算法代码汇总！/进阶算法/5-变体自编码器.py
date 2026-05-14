# 导入必要的库
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
import matplotlib.pyplot as plt
import warnings

# 忽略警告信息
warnings.filterwarnings('ignore')

# 确保使用的是 TensorFlow 2.x
assert tf.__version__.startswith('2'), "请确保使用的是 TensorFlow 2.x 版本。"

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 请确保路径正确
data = pd.read_excel(data_path)

# 2. 数据预处理
# 将最后一列作为目标变量 Y，其余列作为特征 X
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values   # 目标变量

# 对特征进行标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"特征维度: {X_scaled.shape[1]}")
print(f"目标变量样本数: {Y.shape[0]}")

# 3. 定义编码器
latent_dim = 10  # 潜在空间维度，可以根据需要调整

encoder_inputs = layers.Input(shape=(X_scaled.shape[1],), name='encoder_input')
x = layers.Dense(64, activation='relu')(encoder_inputs)
x = layers.Dense(32, activation='relu')(x)
z_mean = layers.Dense(latent_dim, name='z_mean')(x)
z_log_var = layers.Dense(latent_dim, name='z_log_var')(x)

# 自定义采样层
class Sampling(layers.Layer):
    """从潜在空间中采样点。"""
    def call(self, inputs):
        z_mean, z_log_var = inputs
        epsilon = tf.random.normal(shape=tf.shape(z_mean))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

z = Sampling()([z_mean, z_log_var])

# 构建编码器模型
encoder = Model(encoder_inputs, [z_mean, z_log_var, z], name='encoder')
encoder.summary()

# 4. 定义解码器
latent_inputs = layers.Input(shape=(latent_dim,), name='z_sampling')
x = layers.Dense(32, activation='relu')(latent_inputs)
x = layers.Dense(64, activation='relu')(x)
decoder_outputs = layers.Dense(X_scaled.shape[1], activation='linear')(x)

# 构建解码器模型
decoder = Model(latent_inputs, decoder_outputs, name='decoder')
decoder.summary()

# 5. 定义 VAE 模型（子类化）
class VAE(Model):
    def __init__(self, encoder, decoder, input_dim, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.input_dim = input_dim
        # 定义损失跟踪器
        self.total_loss_tracker = tf.keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = tf.keras.metrics.Mean(name="reconstruction_loss")
        self.kl_loss_tracker = tf.keras.metrics.Mean(name="kl_loss")

    def call(self, inputs):
        # 编码
        z_mean, z_log_var, z = self.encoder(inputs)
        # 解码
        reconstruction = self.decoder(z)
        # 计算重构损失（均方误差）
        reconstruction_loss = tf.reduce_mean(tf.square(inputs - reconstruction)) * self.input_dim
        # 计算 KL 散度损失
        kl_loss = -0.5 * tf.reduce_mean(1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
        # 总损失
        total_loss = reconstruction_loss + kl_loss
        # 添加损失到模型
        self.add_loss(total_loss)
        # 更新损失跟踪器
        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)
        return reconstruction

    @property
    def metrics(self):
        return [
            self.total_loss_tracker,
            self.reconstruction_loss_tracker,
            self.kl_loss_tracker,
        ]

# 实例化 VAE 模型
vae = VAE(encoder, decoder, input_dim=X_scaled.shape[1])
vae.compile(optimizer='adam')
vae.summary()

# 6. 训练 VAE 模型
history = vae.fit(
    X_scaled,
    epochs=2000,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# 7. 获取潜在表示并划分数据集
z_mean, z_log_var, z = encoder.predict(X_scaled)
X_latent = z  # 仅使用采样后的 z 作为潜在表示

X_train_latent, X_test_latent, Y_train, Y_test = train_test_split(
    X_latent, Y, test_size=0.2, random_state=42
)

print(f"训练集样本数: {X_train_latent.shape[0]}")
print(f"测试集样本数: {X_test_latent.shape[0]}")

# 8. 构建和训练回归模型
# 定义回归模型
regressor_inputs = layers.Input(shape=(latent_dim,), name='regression_input')
x = layers.Dense(64, activation='relu')(regressor_inputs)
x = layers.Dropout(0.2)(x)
x = layers.Dense(32, activation='relu')(x)
x = layers.Dropout(0.2)(x)
regressor_outputs = layers.Dense(1, activation='linear')(x)

# 构建回归模型
regressor = Model(regressor_inputs, regressor_outputs, name='regressor')
regressor.summary()

# 编译回归模型
regressor.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 训练回归模型
history_reg = regressor.fit(
    X_train_latent, Y_train,
    validation_data=(X_test_latent, Y_test),
    epochs=2000,
    batch_size=32,
    verbose=1
)

# 9. 模型评估
# 进行预测
Y_train_pred = regressor.predict(X_train_latent).flatten()
Y_test_pred = regressor.predict(X_test_latent).flatten()

# 计算评价指标
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    mse = mean_squared_error(Y_true, Y_pred)
    mae = mean_absolute_error(Y_true, Y_pred)
    r2 = r2_score(Y_true, Y_pred)
    evs = explained_variance_score(Y_true, Y_pred)
    print(f"{dataset_type} - MSE: {mse:.4f}")
    print(f"{dataset_type} - MAE: {mae:.4f}")
    print(f"{dataset_type} - R²: {r2:.4f}")
    print(f"{dataset_type} - EVS: {evs:.4f}\n")

print("模型评价指标：")
evaluate_model(Y_train, Y_train_pred, "训练集")
evaluate_model(Y_test, Y_test_pred, "测试集")

# 10. 结果可视化
plt.figure(figsize=(14, 6))

# 训练集对比图
plt.subplot(1, 2, 1)
plt.scatter(Y_train, Y_train_pred, color='blue', alpha=0.5, label='预测值')
plt.plot(
    [Y_train.min(), Y_train.max()],
    [Y_train.min(), Y_train.max()],
    'k--',
    lw=2,
    label='理想情况'
)
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('训练集: 预测值 vs. 真实值')
plt.legend()

# 测试集对比图
plt.subplot(1, 2, 2)
plt.scatter(Y_test, Y_test_pred, color='green', alpha=0.5, label='预测值')
plt.plot(
    [Y_test.min(), Y_test.max()],
    [Y_test.min(), Y_test.max()],
    'k--',
    lw=2,
    label='理想情况'
)
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('测试集: 预测值 vs. 真实值')
plt.legend()

plt.tight_layout()
plt.show()
