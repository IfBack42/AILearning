import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist

# 加载数据集
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 数据预处理：将图像展平成 1D 向量，并将像素值归一化
x_train = x_train.reshape((x_train.shape[0], 28 * 28)).astype('float32') / 255
x_test = x_test.reshape((x_test.shape[0], 28 * 28)).astype('float32') / 255

# 将标签转换为 one-hot 编码
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)
# 构建神经网络模型
model = models.Sequential()

# 输入层和第一个隐藏层：128 个神经元，激活函数为 ReLU
model.add(layers.Dense(128, activation='relu', input_shape=(28 * 28,)))

# 第二个隐藏层：64 个神经元，激活函数为 ReLU
model.add(layers.Dense(64, activation='relu'))

# 输出层：10 个神经元，激活函数为 Softmax，用于多分类任务
model.add(layers.Dense(10, activation='softmax'))
# 编译模型，使用 Adam 优化器，交叉熵损失函数，评估指标为准确率
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
# 训练模型，迭代10次，批次大小为128
model.fit(x_train, y_train, epochs=10, batch_size=128, validation_split=0.2)
# 在测试集上评估模型性能
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"模型在测试集上的准确率: {test_acc:.4f}")
