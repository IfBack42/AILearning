from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# 1. 创建问题实例（最大化问题）
problem = LpProblem("Investment_Problem", LpMaximize)

# 2. 创建0-1决策变量，表示是否选择某个项目
x1 = LpVariable("P1", 0, 1, cat='Binary')  # 项目P1
x2 = LpVariable("P2", 0, 1, cat='Binary')  # 项目P2
x3 = LpVariable("P3", 0, 1, cat='Binary')  # 项目P3
x4 = LpVariable("P4", 0, 1, cat='Binary')  # 项目P4
x5 = LpVariable("P5", 0, 1, cat='Binary')  # 项目P5

# 3. 定义目标函数（最大化总收益）
problem += 15 * x1 + 25 * x2 + 35 * x3 + 45 * x4 + 55 * x5, "Total Profit"

# 4. 添加预算约束
problem += 10 * x1 + 20 * x2 + 30 * x3 + 40 * x4 + 50 * x5 <= 100, "Budget Constraint"

# 5. 求解问题
problem.solve()

# 6. 输出结果
print(f"是否投资项目P1: {x1.varValue}")
print(f"是否投资项目P2: {x2.varValue}")
print(f"是否投资项目P3: {x3.varValue}")
print(f"是否投资项目P4: {x4.varValue}")
print(f"是否投资项目P5: {x5.varValue}")
print(f"最大总收益: {problem.objective.value()} 万美元")
