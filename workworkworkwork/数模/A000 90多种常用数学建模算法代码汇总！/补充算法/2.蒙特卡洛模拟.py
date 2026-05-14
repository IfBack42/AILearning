import numpy as np

# 设定参数
S0 = 100  # 初始股票价格
K = 110   # 执行价格
T = 1.0   # 期权到期时间 (1年)
r = 0.05  # 无风险利率
sigma = 0.2  # 波动率
N = 100000  # 蒙特卡洛模拟的次数

# 使用蒙特卡洛模拟估算期权价格
np.random.seed(42)
Z = np.random.standard_normal(N)  # 标准正态分布随机数
ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)  # 终止价格
payoff = np.maximum(ST - K, 0)  # 看涨期权的支付值

# 贴现支付值的平均作为期权价格
call_price = np.exp(-r * T) * np.mean(payoff)
print(f"蒙特卡洛模拟估算的看涨期权价格: {call_price:.2f}")
