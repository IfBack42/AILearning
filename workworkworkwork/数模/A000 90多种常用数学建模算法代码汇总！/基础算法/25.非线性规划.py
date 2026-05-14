import numpy as np
from scipy.optimize import minimize

# 目标函数（最大化目标，转为最小化问题）
def objective(vars):
    T, P = vars  # 温度和压力
    return -(T - 20)**2 - (P - 30)**2  # 负号表示最大化问题转化为最小化

# 定义约束条件
def constraint1(vars):
    T, P = vars
    return 50 - (T + P)  # T + P <= 50

def constraint2(vars):
    T, P = vars
    return T - 10  # T >= 10

def constraint3(vars):
    T, P = vars
    return P - 15  # P >= 15

# 初始猜测
initial_guess = [25, 25]

# 定义约束条件的形式
constraints = [{'type': 'ineq', 'fun': constraint1},
               {'type': 'ineq', 'fun': constraint2},
               {'type': 'ineq', 'fun': constraint3}]

# 使用minimize函数进行求解
solution = minimize(objective, initial_guess, method='SLSQP', constraints=constraints)

# 输出结果
T_opt, P_opt = solution.x
print(f"最优温度: {T_opt:.2f}")
print(f"最优压力: {P_opt:.2f}")
print(f"最大化生产量: {-solution.fun:.2f}")  # 注意这里取负号，因为我们最小化了负目标函数
