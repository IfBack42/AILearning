from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# 1. 创建问题实例（最大化问题）
problem = LpProblem("Production_Scheduling", LpMaximize)

# 2. 定义连续决策变量（产品的生产量）
x1 = LpVariable("P1_production", lowBound=0)  # 产品P1的生产量
x2 = LpVariable("P2_production", lowBound=0)  # 产品P2的生产量

# 3. 定义二进制决策变量（生产线的启用状态）
y1 = LpVariable("Line_1_status", cat='Binary')  # 生产线1是否启用
y2 = LpVariable("Line_2_status", cat='Binary')  # 生产线2是否启用

# 4. 定义目标函数（最大化利润）
problem += 50 * x1 + 40 * x2 - 1000 * y1 - 800 * y2, "Total Profit"

# 5. 添加约束条件
problem += 3 * x1 + 2 * x2 <= 100, "Labor Constraint"  # 劳动力约束
problem += x1 <= 50 * y1, "Line 1 Capacity Constraint"  # 生产线1容量约束
problem += x2 <= 40 * y2, "Line 2 Capacity Constraint"  # 生产线2容量约束

# 6. 求解问题
problem.solve()

# 7. 输出结果
print(f"产品 P1 的生产量: {x1.varValue}")
print(f"产品 P2 的生产量: {x2.varValue}")
print(f"生产线 1 启动状态: {y1.varValue}")
print(f"生产线 2 启动状态: {y2.varValue}")
print(f"最大总利润: {problem.objective.value()} 美元")
