import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import pandas as pd
from collections import deque
import matplotlib.pyplot as plt

# 读取数据
data_path = "D:/py/LearnPython/data0.xlsx"
data_df = pd.read_excel(data_path)

# 假设数据集的最后一列是输出，其他列是输入特征
input_data = data_df.iloc[:, :-1].values.astype(np.float32)  # 确保输入为 float32
output_data = data_df.iloc[:, -1].values.astype(np.float32)  # 输出为 float32

# 将输入和输出组合为 (输入特征, 输出) 的列表
data = [(input_data[i], output_data[i]) for i in range(len(output_data))]

# 定义动作空间（将连续输出离散化）
min_value = output_data.min()
max_value = output_data.max()
num_actions = 20  # 定义动作的数量，可根据需要调整
action_space = np.linspace(min_value, max_value, num_actions)

# 建立动作索引到实际值的映射
action_to_value = {i: action_space[i] for i in range(num_actions)}

# 定义 Q 网络类
class QNetwork(nn.Module):
    def __init__(self, input_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)  # 输出为动作空间中每个动作的 Q 值

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# 定义 DQN 代理类
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size  # 状态（输入特征）的维度
        self.action_size = action_size  # 动作数量
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # 折扣因子
        self.epsilon = 1.0  # 探索率
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = QNetwork(state_size, action_size)
        self.target_model = QNetwork(state_size, action_size)
        self.update_target_network()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            # 随机选择动作（探索）
            return random.randrange(self.action_size)
        else:
            # 根据模型预测的 Q 值选择动作（利用）
            state = torch.tensor(state, dtype=torch.float32)
            q_values = self.model(state)
            return torch.argmax(q_values).item()

    def train(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        states = []
        targets = []

        for state, action, reward, next_state, done in minibatch:
            state = torch.tensor(state, dtype=torch.float32)
            target = self.model(state).detach().numpy()
            if done:
                target[action] = reward
            else:
                next_state = torch.tensor(next_state, dtype=torch.float32)
                # 使用目标网络计算下一个状态的最大 Q 值
                t = self.target_model(next_state).detach()
                target[action] = reward + self.gamma * torch.max(t).item()
            states.append(state.numpy())
            targets.append(target)

        states = torch.tensor(states, dtype=torch.float32)
        targets = torch.tensor(targets, dtype=torch.float32)

        # 训练模型
        self.optimizer.zero_grad()
        outputs = self.model(states)
        loss = nn.MSELoss()(outputs, targets)
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def update_target_network(self):
        self.target_model.load_state_dict(self.model.state_dict())

# 定义回归任务的环境
class RegressionEnv:
    def __init__(self, data):
        self.data = data
        self.current_step = 0
        self.total_steps = len(data)

    def reset(self):
        self.current_step = 0
        state = self.data[self.current_step][0]
        return state

    def step(self, action_index):
        action_value = action_to_value[action_index]  # 将动作索引转换为实际的预测值
        true_value = self.data[self.current_step][1]
        reward = -abs(true_value - action_value)  # 奖励为负的预测误差
        self.current_step += 1
        done = self.current_step >= self.total_steps
        if not done:
            next_state = self.data[self.current_step][0]
        else:
            next_state = None
        return next_state, reward, done

# 创建回归环境
state_size = input_data.shape[1]  # 输入特征的维度
action_size = num_actions  # 动作数量
env = RegressionEnv(data)

# 创建 DQN 代理
agent = DQNAgent(state_size=state_size, action_size=action_size)

# 训练设置
episodes = 1000
batch_size = 32
losses = []

# 训练过程
for e in range(episodes):
    state = env.reset()
    total_loss = 0
    total_reward = 0

    for time in range(env.total_steps):
        # 行为选择
        action = agent.act(state)
        # 与环境交互
        next_state, reward, done = env.step(action)
        # 记忆存储
        agent.remember(state, action, reward, next_state, done)
        # 更新当前状态
        state = next_state
        total_reward += reward

        # 经验回放训练
        if len(agent.memory) > batch_size:
            loss = agent.train(batch_size)
            total_loss += loss

        if done:
            # 更新目标网络
            agent.update_target_network()
            break

    # 探索率衰减
    if agent.epsilon > agent.epsilon_min:
        agent.epsilon *= agent.epsilon_decay

    # 记录损失和奖励
    losses.append(total_loss)

    # 打印训练信息
    print(f"Episode {e+1}/{episodes}, Total Reward: {total_reward:.2f}, Loss: {total_loss:.4f}, Epsilon: {agent.epsilon:.4f}")

# 绘制损失曲线
plt.plot(losses)
plt.xlabel('Episode')
plt.ylabel('Loss')
plt.title('Training Loss over Episodes')
plt.show()
