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
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values  # 输出（目标变量）

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 将数据划分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

# 3. 构建生成器（Generator）
def build_generator(latent_dim):
    model = tf.keras.Sequential()
    model.add(layers.Dense(256, activation='relu', input_dim=latent_dim))
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(1024, activation='relu'))
    model.add(layers.Dense(1, activation='linear'))  # 输出一个值，匹配Y的维度
    return model

# 4. 构建判别器（Discriminator）
def build_discriminator():
    model = tf.keras.Sequential()
    model.add(layers.Dense(512, activation='relu', input_dim=1))
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model

# 5. 构建GAN模型
def build_gan(generator, discriminator):
    discriminator.trainable = False  # 在训练GAN时，不训练判别器
    gan_input = layers.Input(shape=(generator.input_shape[1],))  # 输入
    generated_data = generator(gan_input)  # 生成数据
    gan_output = discriminator(generated_data)  # 判别器判断生成数据
    gan = Model(gan_input, gan_output)  # 构建GAN模型
    return gan

# 6. 定义超参数
latent_dim = 100  # 随机噪声维度
output_dim = X_train.shape[1]  # 输出维度为输入特征的维度
epochs = 1000  # 训练周期
batch_size = 32
learning_rate = 0.0002
real_label_smooth = 0.9  # 标签平滑，防止判别器过强

# 7. 构建生成器和判别器
generator = build_generator(latent_dim)
discriminator = build_discriminator()
discriminator.compile(optimizer=tf.keras.optimizers.Adam(learning_rate), loss='binary_crossentropy', metrics=['accuracy'])

# 8. 构建并编译GAN
gan = build_gan(generator, discriminator)
gan.compile(optimizer=tf.keras.optimizers.Adam(learning_rate), loss='binary_crossentropy')

# 打印模型结构
print("生成器模型结构：")
generator.summary()  # 打印生成器结构

print("\n判别器模型结构：")
discriminator.summary()  # 打印判别器结构

print("\nGAN模型结构：")
gan.summary()  # 打印GAN模型结构

# 9. 初始化损失记录
d_loss_real_history = []
d_loss_fake_history = []
g_loss_history = []

# 10. 开始训练GAN
real_label = np.ones((batch_size, 1)) * real_label_smooth  # 真实标签为0.9，加入标签平滑
fake_label = np.zeros((batch_size, 1))  # 生成数据标签为0

for epoch in range(epochs):
    # 训练判别器
    idx = np.random.randint(0, X_train.shape[0], batch_size)
    real_data = Y_train[idx].reshape(-1, 1)  # 取Y_train作为真实数据

    noise = np.random.normal(0, 1, (batch_size, latent_dim))  # 生成噪声
    generated_data = generator.predict(noise)

    # 判别器训练
    d_loss_real = discriminator.train_on_batch(real_data, real_label)
    d_loss_fake = discriminator.train_on_batch(generated_data, fake_label)

    # 训练生成器
    noise = np.random.normal(0, 1, (batch_size, latent_dim))
    g_loss = gan.train_on_batch(noise, real_label)

    # 处理g_loss和d_loss，确保它们是浮点数
    if isinstance(g_loss, list):
        g_loss = g_loss[0]
    if isinstance(d_loss_real, list):
        d_loss_real = d_loss_real[0]
    if isinstance(d_loss_fake, list):
        d_loss_fake = d_loss_fake[0]

    # 保存损失
    d_loss_real_history.append(d_loss_real)  # 只保存损失的第一个元素
    d_loss_fake_history.append(d_loss_fake)  # 只保存损失的第一个元素
    g_loss_history.append(g_loss)  # 生成器的损失通常就是一个单独的值

    # 每个epoch打印损失
    print(f"Epoch {epoch+1}/{epochs} - d_loss_real: {d_loss_real:.4f}, d_loss_fake: {d_loss_fake:.4f}, g_loss: {g_loss:.4f}")

# 11. 评估生成器在测试集上的性能
noise = np.random.normal(0, 1, (X_test.shape[0], latent_dim))  # 在测试集上生成数据
generated_data_test = generator.predict(noise)

# 12. 计算4个详细的数字评价指标
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    mse = mean_squared_error(Y_true, Y_pred)  # 均方误差
    mae = mean_absolute_error(Y_true, Y_pred)  # 平均绝对误差
    r2 = r2_score(Y_true, Y_pred)  # R²得分
    evs = explained_variance_score(Y_true, Y_pred)  # 解释方差
    print(f"{dataset_type} - MSE: {mse:.4f}")
    print(f"{dataset_type} - MAE: {mae:.4f}")
    print(f"{dataset_type} - R²: {r2:.4f}")
    print(f"{dataset_type} - EVS: {evs:.4f}\n")

# 评估训练集和测试集的性能
evaluate_model(Y_train, generator.predict(np.random.normal(0, 1, (X_train.shape[0], latent_dim))).flatten(), "训练集")
evaluate_model(Y_test, generated_data_test.flatten(), "测试集")

# 13. 绘制训练过程中损失的变化
plt.figure(figsize=(10, 6))
plt.plot(d_loss_real_history, label='d_loss_real', color='blue', linestyle='--')
plt.plot(d_loss_fake_history, label='d_loss_fake', color='red', linestyle='--')
plt.plot(g_loss_history, label='g_loss', color='green')
plt.title('Training Loss for GAN')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 14. 可视化训练集和测试集的预测值 vs. 真实值
plt.figure(figsize=(14, 6))

# 训练集对比图
plt.subplot(1, 2, 1)
plt.scatter(Y_train, generator.predict(np.random.normal(0, 1, (X_train.shape[0], latent_dim))).flatten(), color='blue', alpha=0.5, label='预测值')
plt.plot([Y_train.min(), Y_train.max()], [Y_train.min(), Y_train.max()], 'k--', lw=2, label='理想情况')
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('训练集: 预测值 vs. 真实值')
plt.legend()

# 测试集对比图
plt.subplot(1, 2, 2)
plt.scatter(Y_test, generated_data_test.flatten(), color='green', alpha=0.5, label='预测值')
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2, label='理想情况')
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('测试集: 预测值 vs. 真实值')
plt.legend()

plt.tight_layout()
plt.show()
