import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
import numpy as np

# 1. 加载 MNIST 数据集
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 2. 数据预处理：将图片展平成 1D 向量，并将像素值归一化到 [0, 1] 范围
x_train = x_train.reshape((x_train.shape[0], 28 * 28)).astype('float32') / 255
x_test = x_test.reshape((x_test.shape[0], 28 * 28)).astype('float32') / 255

# 将标签转换为 one-hot 编码
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

# 3. 构建 BP 神经网络模型
model = models.Sequential()

# 输入层到隐藏层1，128个神经元，激活函数为ReLU
model.add(layers.Dense(128, activation='relu', input_shape=(28 * 28,)))

# 隐藏层1到隐藏层2，64个神经元，激活函数为ReLU
model.add(layers.Dense(64, activation='relu'))

# 隐藏层到输出层，10个神经元，激活函数为Softmax
model.add(layers.Dense(10, activation='softmax'))

# 4. 编译模型，使用交叉熵损失函数，优化器为Adam，评估指标为准确率
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 5. 训练模型
model.fit(x_train, y_train, epochs=10, batch_size=128, validation_split=0.2)

# 6. 在测试集上评估模型
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"模型在测试集上的准确率: {test_acc:.4f}")

# 7. 预测：查看前10个测试样本的预测值
predictions = model.predict(x_test[:10])

# 输出预测结果
for i, prediction in enumerate(predictions):
    print(f"测试样本 {i+1} 预测为: {np.argmax(prediction)}, 实际为: {np.argmax(y_test[i])}")
