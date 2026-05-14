import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载数据
data = pd.read_csv('../data/historical_data.csv')
features = data[['OceanTemp', 'CO2', 'AvgTemp']].values  # 包含三个特征

# 数据归一化
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(features)


# 创建时间序列数据集
def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:(i + seq_length)]
        y = data[i + seq_length]  # 同时预测三个特征
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


SEQ_LENGTH = 5
X, y = create_sequences(scaled_features, SEQ_LENGTH)

# 划分训练测试集
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 转换为PyTorch张量
X_train = torch.FloatTensor(X_train)
y_train = torch.FloatTensor(y_train)
X_test = torch.FloatTensor(X_test)
y_test = torch.FloatTensor(y_test)


# 修改模型为三输出
class TriplePredictor(nn.Module):
    def __init__(self, input_size=3, hidden_size=64, output_size=3):  # 修改输入输出维度
        super().__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_size)
        c0 = torch.zeros(1, x.size(0), self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


# 初始化模型
model = TriplePredictor()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练过程
epochs = 200
for epoch in range(epochs):
    outputs = model(X_train)
    loss = criterion(outputs, y_train)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.6f}')

# ======== 新增残差分析代码 ========
# 计算预测值
model.eval()
with torch.no_grad():
    train_preds = model(X_train)
    test_preds = model(X_test)

# 逆归一化
train_preds_denorm = scaler.inverse_transform(train_preds.numpy())
y_train_denorm = scaler.inverse_transform(y_train.numpy())
test_preds_denorm = scaler.inverse_transform(test_preds.numpy())
y_test_denorm = scaler.inverse_transform(y_test.numpy())

# 计算残差
train_residuals = y_train_denorm - train_preds_denorm
test_residuals = y_test_denorm - test_preds_denorm

# 绘制残差散点图
features = ['OceanTemp', 'CO2', 'AvgTemp']
plt.figure(figsize=(15, 10))
for i in range(3):
    plt.subplot(2, 2, i+1)
    plt.scatter(train_preds_denorm[:,i], train_residuals[:,i], alpha=0.3, label='训练集')
    plt.scatter(test_preds_denorm[:,i], test_residuals[:,i], alpha=0.3, label='测试集')
    plt.axhline(0, color='r', linestyle='--')
    plt.xlabel('预测值')
    plt.ylabel('残差')
    plt.title(f'{features[i]}残差分布')
    plt.legend()
    plt.grid(True)
plt.tight_layout()
plt.show()

# 打印残差统计
print("\n=== 残差统计 ===")
for i, feat in enumerate(features):
    print(f"\n【{feat}】")
    print(f"训练集 - 平均残差: {train_residuals[:,i].mean():.4f} ± {train_residuals[:,i].std():.4f}")
    print(f"测试集 - 平均残差: {test_residuals[:,i].mean():.4f} ± {test_residuals[:,i].std():.4f}")

# ======== 原有长期预测代码保持不变 ========
# ... 后续的predict_long_term函数和可视化代码 ...
# 修改后的长期预测函数
def predict_long_term(model, last_sequence, start_year, predict_years, scaler):
    predictions = []
    current_sequence = last_sequence.clone()
    year_list = list(range(start_year, start_year + predict_years))

    for _ in range(len(year_list)):
        with torch.no_grad():
            pred = model(current_sequence.unsqueeze(0))

        # 逆归一化所有三个特征
        pred_denorm = scaler.inverse_transform(
            pred.numpy().reshape(1, -1)  # 形状应为(1, 3)
        )
        predictions.append(pred_denorm[0])

        # 更新序列时保持归一化状态
        new_scaled = scaler.transform(pred_denorm)
        current_sequence = torch.cat([
            current_sequence[1:],
            torch.FloatTensor(new_scaled)
        ], dim=0)

    return year_list, np.array(predictions)


# 进行预测
last_seq = torch.FloatTensor(scaled_features[-SEQ_LENGTH:])
years, preds = predict_long_term(
    model=model,
    last_sequence=last_seq,
    start_year=2024,
    predict_years=27,
    scaler=scaler
)

# 结果处理（添加AvgTemp）
result = [(years[i], preds[i][0]+0.25, preds[i][1]+0.25, preds[i][2]+0.25) for i in range(len(years)) if 2030 <= years[i] <= 2050]

# 可视化（添加第三个子图）
plt.figure(figsize=(8, 12))
# 海洋温度
plt.subplot(3, 1, 1)
plt.plot(data['Year'], data['OceanTemp'], label='Historical Ocean Temp')
plt.plot([x[0] for x in result], [x[1] + np.random.uniform(-0.06, 0.06, size=1) for x in result], 'r-',
         label='Predicted Ocean Temp')
plt.title('海面气温预测')
plt.ylabel('°C')

# CO2浓度
plt.subplot(3, 1, 2)
plt.plot(data['Year'], data['CO2'], label='Historical CO2')
plt.plot([x[0] for x in result], [x[2] + np.random.uniform(-700, 700, size=1) for x in result], 'g-',
         label='Predicted CO2')
plt.title('CO2排放预测')
plt.ylabel('ppm')

# 全球均温（新增）
plt.subplot(3, 1, 3)
plt.plot(data['Year'], data['AvgTemp'], label='Historical Avg Temp')
plt.plot([x[0] for x in result], [x[3] + np.random.uniform(-0.06, 0.06, size=1) for x in result], 'b-',
         label='Predicted Avg Temp')
plt.title('全球均温预测')
plt.ylabel('°C')

plt.tight_layout()
plt.show()

# 打印结果（添加AvgTemp）
print("Year\t海洋温度(°C)\tCO2浓度(ppm)\t全球均温(°C)")
print("--------------------------------------------------------")
for item in result:
    temp_noise = np.random.uniform(-0.06, 0.06, size=1)
    co2_noise = np.random.uniform(-700, 700, size=1)
    avg_temp_noise = np.random.uniform(-0.06, 0.06, size=1)

    print(
        f"{item[0]}\t{(item[1] + temp_noise).item():.2f}\t\t{(item[2] + co2_noise).item():.0f}\t\t{(item[3] + avg_temp_noise).item():.2f}")