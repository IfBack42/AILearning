import numpy as np
import random

# 定义状态
states = ['晴天', '阴天', '雨天']

# 定义状态转移矩阵
P = np.array([[0.7, 0.2, 0.1],  # 从晴天转移
              [0.5, 0.3, 0.2],  # 从阴天转移
              [0.4, 0.2, 0.4]])  # 从雨天转移

# 初始状态为晴天
initial_state = 0  # 0: 晴天, 1: 阴天, 2: 雨天


# 随机模拟未来的天气变化
def simulate_weather(days, initial_state):
    state = initial_state
    weather_sequence = [states[state]]

    for _ in range(days):
        next_state = np.random.choice([0, 1, 2], p=P[state])
        weather_sequence.append(states[next_state])
        state = next_state

    return weather_sequence


# 模拟未来 10 天的天气变化
days = 10
weather_forecast = simulate_weather(days, initial_state)

# 打印结果
print(f"未来 {days} 天的天气预测:")
for day, weather in enumerate(weather_forecast):
    print(f"第 {day + 1} 天: {weather}")
