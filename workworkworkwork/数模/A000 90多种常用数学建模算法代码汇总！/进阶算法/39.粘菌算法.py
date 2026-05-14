# 导入必要的库
import numpy as np
import matplotlib.pyplot as plt
from mealpy.utils.space import FloatVar
from mealpy.bio_based.SMA import OriginalSMA as SMA  # 只导入粘菌算法

# 定义目标函数和惩罚函数
def objective_function(solution):
    # 目标函数，包含乘除运算
    obj_value = solution[0] * solution[1] * solution[2]

    # 约束条件
    constraint1 = solution[0] + solution[1] + solution[2]

    # 约束1: x1 + x2 + x3 < 50
    if constraint1 >= 50:
        return -99999  # 超过限制时返回惩罚值

    # 约束2: x1 + x2 + x3 > 10
    if constraint1 <= 10:
        return -99999  # 未达到下限时返回惩罚值

    return obj_value  # 符合约束条件时返回目标值

# 定义搜索空间
new_bounds = [(-5, 50), (-10, 100), (-20, 200)]  # 给定搜索空间边界
lb, ub = zip(*new_bounds)  # 提取上下界
bounds = FloatVar(lb=lb, ub=ub, name="delta")  # 定义搜索空间的变量类型

# 定义问题字典
problem_dict = {
    "obj_func": objective_function,  # 指定目标函数
    "bounds": bounds,  # 搜索空间
    "minmax": "max"  # 最大化问题
}

# 只使用粘菌算法（SMA）进行优化
optimizer = SMA(epoch=500, pop_size=100)  # 设置迭代次数和种群大小
best_solution = optimizer.solve(problem_dict)  # 执行优化

# 保存结果
results = {
    "Solution": best_solution.solution,  # 最优解
    "Fitness": best_solution.target.fitness  # 最优解对应的目标值
}

# 保存历史
history = optimizer.history  # 获取优化过程中的历史数据

# 可视化粘菌算法的迭代曲线
def plot_history(history):
    global_best_fit = history.list_global_best_fit  # 获取每代最优目标值
    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.plot(global_best_fit, label="Global Best Fitness", color="blue")  # 绘制曲线
    plt.title("SMA Iteration Curve")  # 设置标题
    plt.xlabel("Epoch")  # 设置x轴标签
    plt.ylabel("Fitness")  # 设置y轴标签
    plt.grid(True)  # 添加网格线
    plt.legend()  # 添加图例
    plt.show()  # 显示图像

# 调用函数绘制迭代曲线
plot_history(history)

# 打印最优解和对应的目标值
print(f"SMA Global Best Solution: {results['Solution']}, Global Best Fitness: {results['Fitness']}")
