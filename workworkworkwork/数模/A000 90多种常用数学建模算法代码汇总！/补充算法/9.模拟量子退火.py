import numpy as np
import matplotlib.pyplot as plt

# 定义5种资产的预期收益率
expected_returns = np.array([0.1, 0.2, 0.15, 0.05, 0.12])

# 定义资产的协方差矩阵（用来衡量风险）
cov_matrix = np.array([
    [0.005, -0.002, 0.004, 0.001, 0.003],
    [-0.002, 0.004, 0.002, -0.001, 0.001],
    [0.004, 0.002, 0.006, 0.000, 0.002],
    [0.001, -0.001, 0.000, 0.005, 0.000],
    [0.003, 0.001, 0.002, 0.000, 0.004]
])

# 风险厌恶系数
risk_aversion = 0.1

# 量子退火的初始温度和冷却率
initial_temperature = 100
cooling_rate = 0.99


# 定义目标函数：计算投资组合的总收益 - 风险
def portfolio_performance(solution, expected_returns, cov_matrix, risk_aversion):
    portfolio_return = np.dot(solution, expected_returns)
    portfolio_risk = np.dot(np.dot(solution.T, cov_matrix), solution)
    return portfolio_return - risk_aversion * portfolio_risk


# 量子退火的模拟实现
def quantum_annealing(expected_returns, cov_matrix, risk_aversion, max_iter=1000, initial_temp=100, cooling_rate=0.99):
    num_assets = len(expected_returns)

    # 初始化解（随机选择投资组合，0表示不投资，1表示投资）
    current_solution = np.random.choice([0, 1], size=num_assets)
    current_value = portfolio_performance(current_solution, expected_returns, cov_matrix, risk_aversion)

    best_solution = np.copy(current_solution)
    best_value = current_value

    temperature = initial_temp
    history = []

    for iteration in range(max_iter):
        # 每次随机选择一个资产进行变动
        new_solution = np.copy(current_solution)
        random_index = np.random.randint(num_assets)
        new_solution[random_index] = 1 - new_solution[random_index]  # 改变当前资产的投资状态

        # 计算新解的收益与风险
        new_value = portfolio_performance(new_solution, expected_returns, cov_matrix, risk_aversion)

        # 判断是否接受新解，根据模拟量子退火的规则，以一定概率接受较差解
        if new_value > current_value:
            accept = True
        else:
            delta = new_value - current_value
            accept = np.random.rand() < np.exp(delta / temperature)  # 类似于量子隧穿效应

        if accept:
            current_solution = new_solution
            current_value = new_value

        # 更新最优解
        if current_value > best_value:
            best_solution = np.copy(current_solution)
            best_value = current_value

        # 降低温度（逐步减弱横场，模拟量子退火的冷却过程）
        temperature *= cooling_rate

        # 记录当前收益与风险
        portfolio_return = np.dot(current_solution, expected_returns)
        portfolio_risk = np.dot(np.dot(current_solution.T, cov_matrix), current_solution)
        history.append((portfolio_return, portfolio_risk))

    return best_solution, best_value, history


# 参数设置
max_iter = 1000
initial_temp = 100
cooling_rate = 0.99

# 运行量子退火模拟
best_solution, best_value, history = quantum_annealing(expected_returns, cov_matrix, risk_aversion, max_iter,
                                                       initial_temp, cooling_rate)

# 输出最优解
print("最优投资组合:", best_solution)
portfolio_return = np.dot(best_solution, expected_returns)
portfolio_risk = np.dot(np.dot(best_solution.T, cov_matrix), best_solution)
print(f"投资组合的预期收益: {portfolio_return:.2f}")
print(f"投资组合的风险 (波动率): {portfolio_risk:.2f}")

# 绘制收益与风险的变化过程
history_returns = [h[0] for h in history]
history_risks = [h[1] for h in history]

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(history_returns)
plt.title("投资组合收益变化")
plt.xlabel("迭代次数")
plt.ylabel("预期收益")

plt.subplot(1, 2, 2)
plt.plot(history_risks)
plt.title("投资组合风险变化")
plt.xlabel("迭代次数")
plt.ylabel("风险 (波动率)")

plt.tight_layout()
plt.show()
