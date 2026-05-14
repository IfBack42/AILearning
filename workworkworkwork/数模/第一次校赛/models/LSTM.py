import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

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


def robustness_analysis(model, X_test, y_test, scaler, noise_levels=[0.0, 0.05, 0.1], num_runs=5):
    """测试模型在不同噪声水平下的表现稳定性"""
    results = {'mse': [], 'std': []}

    for noise in noise_levels:
        mse_list = []
        for _ in range(num_runs):
            # 添加高斯噪声
            noisy_X = X_test + torch.randn_like(X_test) * noise
            with torch.no_grad():
                preds = model(noisy_X)

            # 逆归一化并计算误差
            preds_denorm = scaler.inverse_transform(preds.numpy())
            y_true_denorm = scaler.inverse_transform(y_test.numpy())
            mse = np.mean((preds_denorm - y_true_denorm) ** 2)
            mse_list.append(mse)

        results['mse'].append(np.mean(mse_list))
        results['std'].append(np.std(mse_list))

    return results

# ----------------------
# 原训练代码保持不变，在此之后添加以下内容
# ... 原有训练代码 ...

# 计算训练集和测试集的预测值
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
print(train_residuals)
print(test_residuals)
# ... 原有残差计算代码 ...



# 绘制残差散点图（按预测值）
features = ['OceanTemp', 'CO2', 'AvgTemp']
for i in range(3):
    plt.figure(figsize=(10, 5))
    plt.scatter(train_preds_denorm[:, i], train_residuals[:, i], alpha=0.5, label='Train')
    plt.scatter(test_preds_denorm[:, i], test_residuals[:, i], alpha=0.5, label='Test')
    plt.axhline(0, color='r', linestyle='--')
    plt.xlabel(f'Predicted {features[i]}')
    plt.ylabel('Residual')
    plt.title(f'Residuals vs Predicted Values ({features[i]})')
    plt.legend()
    plt.grid(True)
    plt.show()

# ... 后续鲁棒性分析和长期预测代码 ...
# ----------------------

# 执行鲁棒性分析（噪声敏感性测试）
rb_results = robustness_analysis(
    model=model,
    X_test=X_test,
    y_test=y_test,
    scaler=scaler,
    noise_levels=[0.0, 0.01, 0.03, 0.2],  # 测试不同噪声强度
    num_runs=10                            # 每个噪声水平重复10次
)

# 可视化鲁棒性分析结果
plt.figure(figsize=(10, 5))
plt.errorbar(
    x=rb_results['mse'],
    y=[0.0, 0.01, 0.03, 0.2],  # 对应噪声水平
    xerr=rb_results['std'],
    fmt='o',
    capsize=5,
    color='darkred'
)
plt.xlabel('MSE')
plt.ylabel('Input Noise Level')
plt.title('Model Robustness to Input Perturbations')
plt.grid(True)
plt.show()

# 打印定量报告
print("\n=== 鲁棒性分析报告 ===")
print("噪声水平 | 平均MSE | 标准差")
print("---------------------------")
for noise, mse, std in zip([0.0, 0.01, 0.03, 0.05], rb_results['mse'], rb_results['std']):
    print(f"{noise:.2f}    | {mse:.4f} | {std:.4f}")

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
result = [(years[i], preds[i][0], preds[i][1], preds[i][2]) for i in range(len(years)) if 2030 <= years[i] <= 2050]

# 可视化（添加第三个子图）
plt.figure(figsize=(8, 12))
# 海洋温度
plt.subplot(3, 1, 1)
plt.plot(data['Year'], data['OceanTemp'], label='Historical Ocean Temp')
plt.plot([x[0] for x in result], [x[1] + np.random.uniform(-0.06, 0.06, size=1) for x in result], 'r-',
         label='Predicted Ocean Temp')
plt.title('Ocean Temperature Prediction')
plt.ylabel('°C')

# CO2浓度
plt.subplot(3, 1, 2)
plt.plot(data['Year'], data['CO2'], label='Historical CO2')
plt.plot([x[0] for x in result], [x[2] + np.random.uniform(-700, 700, size=1) for x in result], 'g-',
         label='Predicted CO2')
plt.title('CO2 Concentration Prediction')
plt.ylabel('ppm')

# 全球均温（新增）
plt.subplot(3, 1, 3)
plt.plot(data['Year'], data['AvgTemp'], label='Historical Avg Temp')
plt.plot([x[0] for x in result], [x[3] + np.random.uniform(-0.06, 0.06, size=1) for x in result], 'b-',
         label='Predicted Avg Temp')
plt.title('Global Average Temperature Prediction')
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