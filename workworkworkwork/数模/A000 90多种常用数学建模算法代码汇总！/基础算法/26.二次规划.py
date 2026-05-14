import numpy as np
from scipy.optimize import minimize

# 定义目标函数 (1/2) * x^T * Q * x
def objective(x):
    Q = np.array([[0.1, 0.01, 0.02],
                  [0.01, 0.2, 0.03],
                  [0.02, 0.03, 0.3]])  # 协方差矩阵
    return 0.5 * np.dot(x.T, np.dot(Q, x))

# 定义收益率约束 0.10x_1 + 0.20x_2 + 0.15x_3 = 0.15
def constraint1(x):
    return np.dot([0.10, 0.20, 0.15], x) - 0.15

# 定义总投资约束 x_1 + x_2 + x_3 = 1
def constraint2(x):
    return np.sum(x) - 1

# 定义初始猜测值（初始投资比例）
initial_guess = [1/3, 1/3, 1/3]

# 定义约束条件
constraints = [{'type': 'eq', 'fun': constraint1},  # 收益率约束
               {'type': 'eq', 'fun': constraint2}]  # 投资总金额约束

# 定义非负约束 (x_1, x_2, x_3 >= 0)
bounds = [(0, None), (0, None), (0, None)]

# 使用 SciPy 的 minimize 函数进行优化求解
solution = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

# 输出结果
print("最优投资比例:")
print(f"资产 A1: {solution.x[0]:.4f}")
print(f"资产 A2: {solution.x[1]:.4f}")
print(f"资产 A3: {solution.x[2]:.4f}")
print(f"最小化的风险值: {solution.fun:.4f}")
