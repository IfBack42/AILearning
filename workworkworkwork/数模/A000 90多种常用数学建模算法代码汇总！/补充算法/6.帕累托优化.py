import numpy as np
import matplotlib.pyplot as plt

# 生成模拟数据：时间和成本的解
np.random.seed(42)
n_points = 100  # 生成 100 个解
time = np.random.rand(n_points) * 10 + 10  # 时间（10到20之间随机）
cost = np.random.rand(n_points) * 1000 + 10000  # 成本（10000到11000之间随机）

# 绘制初始的时间-成本分布
plt.figure(figsize=(8, 6))
plt.scatter(time, cost, color='gray', label='所有解')
plt.xlabel('项目完成时间', fontsize=12)
plt.ylabel('项目成本', fontsize=12)
plt.title('项目的时间与成本解空间', fontsize=14)
plt.grid(True)
plt.legend()
plt.show()

# 帕累托优化函数
def pareto_optimization(time, cost):
    is_pareto = np.ones(time.shape[0], dtype=bool)  # 初始化所有解为帕累托最优
    for i in range(time.shape[0]):
        for j in range(time.shape[0]):
            if (time[j] < time[i] and cost[j] <= cost[i]) or (time[j] <= time[i] and cost[j] < cost[i]):
                # 如果解 j 支配解 i，标记解 i 不是帕累托最优
                is_pareto[i] = False
                break
    return is_pareto

# 计算帕累托前沿
pareto_mask = pareto_optimization(time, cost)

# 绘制帕累托前沿
plt.figure(figsize=(8, 6))
plt.scatter(time, cost, color='gray', alpha=0.5, label='所有解')
plt.scatter(time[pareto_mask], cost[pareto_mask], color='red', label='帕累托前沿', s=50)
plt.xlabel('项目完成时间', fontsize=12)
plt.ylabel('项目成本', fontsize=12)
plt.title('帕累托前沿：项目完成时间与成本的平衡', fontsize=14)
plt.grid(True)
plt.legend()
plt.show()

# 打印帕累托前沿解
print("帕累托前沿解 (项目时间，项目成本)：")
for t, c in zip(time[pareto_mask], cost[pareto_mask]):
    print(f"时间: {t:.2f}, 成本: {c:.2f}")
