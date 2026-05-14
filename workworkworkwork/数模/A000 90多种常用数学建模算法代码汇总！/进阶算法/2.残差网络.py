import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. 读取数据
# 使用pandas读取Excel文件中的数据
# path_to_file是你的Excel文件的路径，确保文件格式正确
file_path = 'D:/py/LearnPython/data0.xlsx'
data = pd.read_excel(file_path)

# 2. 数据预处理
# 将最后一列作为输出y，其他列作为输入X
X = data.iloc[:, :-1].values  # 输入数据，所有列除了最后一列
y = data.iloc[:, -1].values   # 输出数据，最后一列

# 3. 数据标准化（对输入特征进行标准化）
# 标准化是为了让所有特征值范围相近，避免某些特征对模型训练造成过大影响
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 4. 将数据分为训练集和测试集
# train_test_split将数据随机分为训练集和测试集，test_size=0.2表示20%的数据作为测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 将数据转换为Tensor格式，以便PyTorch使用
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)  # 需要将y转换为二维的（N, 1）
y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# 5. 定义残差块（Residual Block）
# 残差块包含两层全连接层和一个残差连接，跳跃连接避免梯度消失
class ResidualBlock(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(ResidualBlock, self).__init__()
        self.fc1 = nn.Linear(input_dim, output_dim)  # 第一层全连接层
        self.relu = nn.ReLU()  # ReLU激活函数
        self.dropout = nn.Dropout(0.3)  # Dropout层防止过拟合
        self.fc2 = nn.Linear(output_dim, output_dim)  # 第二层全连接层

    def forward(self, x):
        identity = x  # 跳跃连接中的输入
        out = self.fc1(x)  # 通过第一层全连接层
        out = self.relu(out)  # ReLU激活
        out = self.dropout(out)  # Dropout防止过拟合
        out = self.fc2(out)  # 通过第二层全连接层
        out += identity  # 残差连接，直接将输入加到输出上
        return self.relu(out)  # 再次通过ReLU激活

# 6. 定义复杂残差网络模型（包含多个残差块）
class ComplexResNetRegressor(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(ComplexResNetRegressor, self).__init__()
        self.input_layer = nn.Linear(input_dim, 128)  # 输入层，输入维度到128维
        self.res_block1 = ResidualBlock(128, 128)  # 第一层残差块
        self.res_block2 = ResidualBlock(128, 128)  # 第二层残差块
        self.res_block3 = ResidualBlock(128, 128)  # 第三层残差块
        self.output_layer = nn.Linear(128, output_dim)  # 输出层，128维到1维（输出预测的房价）

    def forward(self, x):
        x = self.input_layer(x)  # 输入层处理
        x = self.res_block1(x)  # 通过第一层残差块
        x = self.res_block2(x)  # 通过第二层残差块
        x = self.res_block3(x)  # 通过第三层残差块
        x = self.output_layer(x)  # 最后通过输出层得到结果
        return x

# 7. 初始化模型、损失函数和优化器
model = ComplexResNetRegressor(input_dim=X_train.shape[1], output_dim=1)  # 输入维度为特征数量，输出为1个预测值
criterion = nn.MSELoss()  # 均方误差损失函数，用于回归任务
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)  # Adam优化器，使用L2正则化

# 8. 训练模型
num_epochs = 2000  # 训练200个epoch
for epoch in range(num_epochs):
    model.train()  # 设置模型为训练模式
    optimizer.zero_grad()  # 梯度清零
    outputs = model(X_train)  # 前向传播，得到预测结果
    loss = criterion(outputs, y_train)  # 计算损失
    loss.backward()  # 反向传播计算梯度
    optimizer.step()  # 更新模型参数

    # 每20个epoch打印一次损失
    if (epoch + 1) % 20 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 9. 测试模型
model.eval()  # 设置模型为评估模式
with torch.no_grad():  # 测试时不计算梯度
    predicted = model(X_test)  # 对测试集进行预测
    test_loss = criterion(predicted, y_test)  # 计算测试集上的损失
    print(f'Test Loss: {test_loss.item():.4f}')

# 10. 打印部分预测结果和真实结果对比
predicted = predicted.numpy()  # 将预测结果转换为numpy格式，方便输出
y_test = y_test.numpy()  # 同样将真实结果转换为numpy格式
print("\n预测值 vs 实际值:")
for i in range(10):  # 打印前10个测试集样本的预测值和实际值对比
    print(f"预测值: {predicted[i][0]:.2f}, 实际值: {y_test[i][0]:.2f}")
