import numpy as np
from scipy.optimize import linprog

# 1. 定义目标函数的系数（负号表示最大化问题转换为最小化）
c = [-3, -5]

# 2. 定义不等式约束的系数矩阵和右侧的常数
A = [[2, 3],  # 劳动力约束
     [1, 2]]  # 原材料约束
b = [120, 100]

# 3. 定义决策变量的非负约束
x0_bounds = (0, None)
x1_bounds = (0, None)

# 4. 使用 linprog 求解线性规划问题
result = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='highs')

# 5. 输出结果
print(f"最大化利润时，P1 的生产量为: {result.x[0]:.2f} 单位")
print(f"最大化利润时，P2 的生产量为: {result.x[1]:.2f} 单位")
print(f"最大化的利润为: {-result.fun:.2f} 美元")
