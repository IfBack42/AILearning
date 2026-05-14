# 导入必要的库
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.applications import Xception
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
import matplotlib.pyplot as plt
import os

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'
data = pd.read_excel(data_path)

# 2. 数据预处理
# 将最后一列作为目标变量Y，其余列作为特征X
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values  # 目标变量

# 3. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# 4. 将数值数据转换为图像格式
def reshape_to_image(X, image_size=(71, 71)):
    """
    将数值型数据重塑为二维图像格式，并扩展为3个通道。

    参数:
        X (numpy.ndarray): 输入特征，形状为 (样本数量, 特征数量)
        image_size (tuple): 目标图像大小 (高度, 宽度)

    返回:
        numpy.ndarray: 重塑后的数据，形状为 (样本数量, 高度, 宽度, 3)
    """
    num_samples, num_features = X.shape
    height, width = image_size
    total_pixels = height * width

    if num_features > total_pixels:
        raise ValueError(
            f"特征数量 ({num_features}) 超过目标图像像素数量 ({total_pixels})。请增加图像大小或减少特征数量。")

    # 初始化为零
    X_padded = np.zeros((num_samples, total_pixels))
    X_padded[:, :num_features] = X  # 填充实际数据

    # 重塑为 (样本数量, 高度, 宽度)
    X_reshaped = X_padded.reshape(num_samples, height, width)

    # 扩展维度以匹配通道数 (样本数量, 高度, 宽度, 1)
    X_reshaped = np.expand_dims(X_reshaped, axis=-1)

    # 复制通道，得到 (样本数量, 高度, 宽度, 3)
    X_image = np.repeat(X_reshaped, 3, axis=-1)

    return X_image


# 应用重塑函数
image_size = (71, 71)  # Xception的最小输入尺寸
X_images = reshape_to_image(X_scaled, image_size=image_size)

# 5. 划分训练集和测试集
X_train_img, X_test_img, Y_train, Y_test = train_test_split(
    X_images, Y, test_size=0.2, random_state=42
)

# 6. 构建Xception模型
# 使用自定义输入层
input_tensor = Input(shape=(image_size[0], image_size[1], 3))
# 不使用预训练权重
base_model = Xception(include_top=False, weights=None, input_tensor=input_tensor, pooling='avg')

# 添加输出层，进行回归任务
x = base_model.output
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
output = Dense(1, activation='linear')(x)

# 定义完整的模型
model = Model(inputs=base_model.input, outputs=output)

# 7. 编译模型
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 8. 训练模型
history = model.fit(
    X_train_img, Y_train,
    validation_data=(X_test_img, Y_test),
    epochs=50,
    batch_size=32,
    verbose=1
)

# 9. 进行预测
Y_train_pred = model.predict(X_train_img)
Y_test_pred = model.predict(X_test_img)


# 10. 计算评价指标
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):
    """
    计算并打印评价指标。

    参数:
        Y_true (numpy.ndarray): 真实目标值
        Y_pred (numpy.ndarray): 预测目标值
        dataset_type (str): 数据集类型标识（例如 '训练集'）
    """
    mse = mean_squared_error(Y_true, Y_pred)
    mae = mean_absolute_error(Y_true, Y_pred)
    r2 = r2_score(Y_true, Y_pred)
    evs = explained_variance_score(Y_true, Y_pred)
    print(f"{dataset_type} - MSE: {mse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}, EVS: {evs:.4f}")


print("模型评价指标：")
evaluate_model(Y_train, Y_train_pred, "训练集")
evaluate_model(Y_test, Y_test_pred, "测试集")

# 11. 绘制预测值与真实值的对比图
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))

# 训练集对比图
plt.subplot(1, 2, 1)
plt.scatter(Y_train, Y_train_pred, color='blue', alpha=0.5, label='预测值')
plt.plot(
    [Y_train.min(), Y_train.max()],
    [Y_train.min(), Y_train.max()],
    'k--',
    lw=2,
    label='真实值'
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
    label='真实值'
)
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('测试集: 预测值 vs. 真实值')
plt.legend()

plt.tight_layout()
plt.show()
