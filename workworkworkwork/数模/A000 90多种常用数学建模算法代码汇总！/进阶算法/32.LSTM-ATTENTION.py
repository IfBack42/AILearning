# 导入必要的库
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Attention, Concatenate, Flatten
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 数据文件路径
data = pd.read_excel(data_path)  # 读取Excel文件

# 将数据分为输入（X）和输出（y）
X = data.iloc[:, :-1].values  # 输入特征，最后一列之外的数据
y = data.iloc[:, -1].values  # 输出特征，最后一列

# 数据标准化
scaler_X = StandardScaler()  # 初始化输入数据标准化器
scaler_y = StandardScaler()  # 初始化输出数据标准化器
X_scaled = scaler_X.fit_transform(X)  # 标准化输入数据
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))  # 标准化输出数据


# 定义LSTM-Attention模型
def build_lstm_attention_model(input_shape):
    """
    构建LSTM-Attention模型，用于时间序列预测
    """
    inputs = Input(shape=input_shape)  # 输入层，输入为时间序列

    # LSTM层，保留时间步输出，确保Attention层接收3D输入
    lstm_out = LSTM(128, return_sequences=True)(inputs)

    # Attention机制，输入和输出必须是3D
    attention_out = Attention()([lstm_out, lstm_out])

    # 将LSTM和Attention的输出进行Flatten处理，以便后续使用Dense层
    flatten_out = Flatten()(attention_out)

    # 输出层
    outputs = Dense(1)(flatten_out)

    # 构建模型并编译
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer=Adam(), loss='mse', metrics=['mae'])

    return model


# 构建LSTM-Attention模型
input_shape = (X_scaled.shape[1], 1)
model = build_lstm_attention_model(input_shape)

# 模型训练
history = model.fit(X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1), y_scaled, epochs=1000, batch_size=64,
                    validation_split=0.2)

# 预测
y_pred_scaled = model.predict(X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1))

# 修正预测结果的维度，将三维数组转换为二维数组
y_pred_scaled = np.squeeze(y_pred_scaled)  # 去除不必要的维度

# 将预测值反标准化为原始数据
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))

# 可视化结果
plt.figure(figsize=(10, 6))
plt.plot(y, label='真实值')
plt.plot(y_pred, label='预测值')
plt.title('真实值与预测值对比')
plt.xlabel('样本')
plt.ylabel('输出')
plt.legend()
plt.show()

# 模型性能评价
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y, y_pred)
mae = mean_absolute_error(y, y_pred)
r2 = r2_score(y, y_pred)

print(f'MSE: {mse}')
print(f'MAE: {mae}')
print(f'R2 Score: {r2}')
