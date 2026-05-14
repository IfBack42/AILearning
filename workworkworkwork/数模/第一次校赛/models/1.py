import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


# 新增鲁棒性分析函数
def robustness_analysis(model, X_test, y_test, scaler, noise_levels=[0.0, 0.05, 0.1], num_runs=5):
    """模型鲁棒性测试：不同噪声水平下的性能变化"""
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
# 原数据加载与预处理部分保持不变
# ----------------------
data = pd.read_csv('../data/historical_data.csv')
features = data[['OceanTemp', 'CO2', 'AvgTemp']].values

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(features)

SEQ_LENGTH = 5


def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:(i + seq_length)]
        y = data[i + seq_length]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


X, y = create_sequences(scaled_features, SEQ_LENGTH)
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

X_train = torch.FloatTensor(X_train)
y_train = torch.FloatTensor(y_train)
X_test = torch.FloatTensor(X_test)
y_test = torch.FloatTensor(y_test)


# ----------------------
# 原模型定义与训练保持不变
# ----------------------
class TriplePredictor(nn.Module):
    def __init__(self, input_size=3, hidden_size=64, output_size=3):
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


model = TriplePredictor()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

epochs = 200
for epoch in range(epochs):
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 20 == 0:
        print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.6f}')

# ----------------------
# 新增鲁棒性分析执行
# ----------------------
# 执行噪声敏感性测试
rb_results = robustness_analysis(model, X_test, y_test, scaler,
                                 noise_levels=[0.0, 0.01, 0.03, 0.05],
                                 num_runs=10)

# 可视化噪声敏感性
plt.figure(figsize=(10, 5))
plt.errorbar(x=rb_results['mse'],
             y=[0.01, 0.03, 0.05, 0.07],  # 对齐噪声水平
             xerr=rb_results['std'],
             fmt='o',
             capsize=5,
             color='darkred')
plt.xlabel('MSE')
plt.ylabel('Noise Level')
plt.title('Model Robustness to Input Noise')
plt.grid(True)
plt.show()

# 打印鲁棒性报告
print("\n=== 鲁棒性分析报告 ===")
print("噪声水平 | 平均MSE | 标准差")
print("---------------------------")
for noise, mse, std in zip([0.01, 0.03, 0.05, 0.07], rb_results['mse'], rb_results['std']):
    print(f"{noise:.2f}    | {mse:.4f} | {std:.4f}")

# ----------------------
# 原预测与可视化部分保持不变
# ----------------------
# ...（原有预测和可视化代码保持不变）...