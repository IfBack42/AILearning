from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# 1. 创建问题实例（最大化问题）
problem = LpProblem("Maximize_Profit", LpMaximize)

# 2. 创建决策变量，并设置为非负整数
x1 = LpVariable("P1", lowBound=0, cat='Integer')  # P1的生产数量
x2 = LpVariable("P2", lowBound=0, cat='Integer')  # P2的生产数量

# 3. 定义目标函数（最大化利润）
problem += 40 * x1 + 30 * x2, "Total Profit"

# 4. 添加约束条件
problem += 2 * x1 + x2 <= 100, "Labor Constraint"
problem += x1 + 2 * x2 <= 80, "Material Constraint"

# 5. 求解问题
problem.solve()

# 6. 输出结果
print(f"生产 P1 的数量: {x1.varValue}")
print(f"生产 P2 的数量: {x2.varValue}")
print(f"最大利润: {problem.objective.value()} 美元")
