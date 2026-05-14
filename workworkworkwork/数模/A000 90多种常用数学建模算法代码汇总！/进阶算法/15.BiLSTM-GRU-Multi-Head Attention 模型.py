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
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values   # 输出（目标变量）

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 将数据划分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.2, random_state=42)

# 3. 构建复杂的深度学习模型
def build_complex_model(input_shape):
    inputs = layers.Input(shape=input_shape)

    # 第一层：更大的全连接层
    x = layers.Dense(512, activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)

    # 第二层：更大的全连接层
    x = layers.Dense(256, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)

    # 第三层：增加一个全连接层
    x = layers.Dense(128, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)

    # 第四层：增加一个全连接层
    x = layers.Dense(64, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)

    # 输出层
    outputs = layers.Dense(1, activation='linear')(x)

    model = Model(inputs=inputs, outputs=outputs)
    return model

# 4. 构建并编译模型
input_shape = (X_train.shape[1],)  # 输入形状
model = build_complex_model(input_shape)

# 使用 Huber 损失函数和 Adam 优化器，增加学习率
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.005),
              loss=tf.keras.losses.Huber(),
              metrics=['mae'])

# 打印模型结构
model.summary()

# 5. 训练模型（取消早停机制，增加训练轮数）
history = model.fit(X_train, Y_train,
                    epochs=500,
                    batch_size=16,  # 减小批次大小
                    validation_split=0.2,
                    verbose=1)

# 6. 模型评估
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

# 7. 绘制训练过程中的损失曲线
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='训练损失')
plt.plot(history.history['val_loss'], label='验证损失')
plt.title('模型训练过程中的损失曲线')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

# 8. 绘制训练集和测试集的预测值 vs. 真实值
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
