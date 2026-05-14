import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. 读取数据
file_path = 'D:/py/LearnPython/data0.xlsx'
data = pd.read_excel(file_path)

# 2. 数据预处理
X = data.iloc[:, :-1].values  # 输入数据，所有列除了最后一列
y = data.iloc[:, -1].values   # 输出数据，最后一列

# 3. 数据标准化（对输入特征进行标准化）
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 4. 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 将数据转换为Tensor格式
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# 获取特征数量
num_features = X_train.shape[1]

# 调整输入数据的形状以适应卷积层 [batch_size, channels, height, width]
# 将特征维度作为宽度，高度为1，通道数为1
X_train = X_train.unsqueeze(1).unsqueeze(2)  # [batch_size, 1, 1, num_features]
X_test = X_test.unsqueeze(1).unsqueeze(2)

# 5. 定义Inception模块
class InceptionModule(nn.Module):
    def __init__(self, in_channels):
        super(InceptionModule, self).__init__()

        # 1x1卷积分支
        self.branch1x1 = nn.Conv2d(in_channels, 64, kernel_size=1)

        # 1x1卷积后接1x3卷积分支
        self.branch3x3 = nn.Sequential(
            nn.Conv2d(in_channels, 96, kernel_size=1),
            nn.Conv2d(96, 128, kernel_size=(1, 3), padding=(0, 1))
        )

        # 1x1卷积后接1x5卷积分支
        self.branch5x5 = nn.Sequential(
            nn.Conv2d(in_channels, 16, kernel_size=1),
            nn.Conv2d(16, 32, kernel_size=(1, 5), padding=(0, 2))
        )

        # 最大池化后接1x1卷积分支
        self.branch_pool = nn.Sequential(
            nn.MaxPool2d(kernel_size=(1, 3), stride=1, padding=(0, 1)),
            nn.Conv2d(in_channels, 32, kernel_size=1)
        )

    def forward(self, x):
        branch1x1 = self.branch1x1(x)
        branch3x3 = self.branch3x3(x)
        branch5x5 = self.branch5x5(x)
        branch_pool = self.branch_pool(x)

        # 在通道维度上拼接输出
        outputs = [branch1x1, branch3x3, branch5x5, branch_pool]
        return torch.cat(outputs, 1)

# 6. 定义Inception网络
class InceptionNet(nn.Module):
    def __init__(self, num_features):
        super(InceptionNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 192, kernel_size=(1, 3), padding=(0, 1))
        self.inception1 = InceptionModule(192)
        self.inception2 = InceptionModule(256)
        # 计算全连接层的输入尺寸
        self.fc_input_dim = 256 * 1 * num_features
        self.fc = nn.Linear(self.fc_input_dim, 1)

    def forward(self, x):
        x = self.conv1(x)
        x = self.inception1(x)
        x = self.inception2(x)
        x = x.view(x.size(0), -1)  # 展平
        x = self.fc(x)
        return x

# 7. 初始化模型、损失函数和优化器
model = InceptionNet(num_features)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 8. 训练模型
num_epochs = 200
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 9. 测试模型
model.eval()
with torch.no_grad():
    predicted = model(X_test)
    test_loss = criterion(predicted, y_test)
    print(f'Test Loss: {test_loss.item():.4f}')

# 10. 打印部分预测结果和真实结果对比
predicted = predicted.numpy()
y_test = y_test.numpy()
print("\n预测值 vs 实际值:")
for i in range(min(10, len(predicted))):
    print(f"预测值: {predicted[i][0]:.2f}, 实际值: {y_test[i][0]:.2f}")
