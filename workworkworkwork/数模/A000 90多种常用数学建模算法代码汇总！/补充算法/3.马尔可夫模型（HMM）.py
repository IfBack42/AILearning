import numpy as np
from hmmlearn import hmm

# 定义状态和观测值
states = ["晴天", "阴天", "雨天"]
observations = ["高温", "中温", "低温"]

# 定义状态转移概率矩阵
transition_matrix = np.array([[0.7, 0.2, 0.1],  # 从晴天转移
                              [0.4, 0.4, 0.2],  # 从阴天转移
                              [0.3, 0.3, 0.4]]) # 从雨天转移

# 定义观测概率矩阵（观测值对应高温、中温、低温）
emission_matrix = np.array([[0.8, 0.1, 0.1],  # 晴天：高温、中温、低温的概率
                            [0.2, 0.6, 0.2],  # 阴天：高温、中温、低温的概率
                            [0.1, 0.3, 0.6]]) # 雨天：高温、中温、低温的概率

# 定义初始状态分布
start_prob = np.array([0.6, 0.3, 0.1])  # 初始为晴天的概率最高

# 创建MultinomialHMM模型，并设置n_trials为1
model = hmm.MultinomialHMM(n_components=3, n_trials=1)
model.startprob_ = start_prob
model.transmat_ = transition_matrix
model.emissionprob_ = emission_matrix

# 修改观测序列为one-hot编码形式
# 观测到的温度序列：高温、中温、低温
obs_sequence = np.array([[1, 0, 0],  # 高温
                         [0, 1, 0],  # 中温
                         [0, 0, 1]]) # 低温

# 使用Viterbi算法解码，找到最有可能的天气（隐状态）序列
logprob, weather_sequence = model.decode(obs_sequence, algorithm="viterbi")

# 打印结果
print("观测到的温度序列:", [observations[np.argmax(obs)] for obs in obs_sequence])
print("最有可能的天气序列:", [states[i] for i in weather_sequence])
