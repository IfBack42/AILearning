import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

# 1. 加载自定义字体
font_path = r'C:\Users\12595\Desktop\STZHONGS.TTF'  # 你的字体路径
custom_font = font_manager.FontProperties(fname=font_path)

# 2. 定义两个目标函数
def objective_1(x):
    return x ** 2

def objective_2(x):
    return (x - 2) ** 2

# 3. 定义种群大小
population_size = 50
num_generations = 100

# 4. 初始化种群，随机生成 [-10, 10] 范围内的解
population = np.random.uniform(-10, 10, population_size)

# 5. NSGA-II 算法中的非支配排序
def non_dominated_sorting(objectives):
    population_size = objectives.shape[0]
    fronts = [[]]  # 用于存储帕累托前沿
    domination_count = np.zeros(population_size)  # 每个个体被支配的数量
    dominated_solutions = [[] for _ in range(population_size)]  # 每个个体支配的解集

    for p in range(population_size):
        for q in range(population_size):
            if all(objectives[p] <= objectives[q]) and any(objectives[p] < objectives[q]):
                dominated_solutions[p].append(q)
            elif all(objectives[q] <= objectives[p]) and any(objectives[q] < objectives[p]):
                domination_count[p] += 1

        if domination_count[p] == 0:
            fronts[0].append(p)

    i = 0
    while fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in dominated_solutions[p]:
                domination_count[q] -= 1
                if domination_count[q] == 0:
                    next_front.append(q)
        i += 1
        fronts.append(next_front)

    fronts.pop()  # 删除最后一个空列表
    return fronts

# 6. 计算拥挤距离
def crowding_distance_assignment(objectives, front):
    distance = np.zeros(len(front))
    for m in range(objectives.shape[1]):
        sorted_idx = np.argsort(objectives[front, m])
        distance[0] = distance[-1] = float('inf')
        for i in range(1, len(front) - 1):
            distance[i] += (objectives[front, sorted_idx[i + 1], m] - objectives[front, sorted_idx[i - 1], m])
    return distance

# 7. 适应度计算和选择
def nsga_ii_selection(population, objectives, fronts):
    next_population = []
    for front in fronts:
        if len(next_population) + len(front) <= population_size:
            next_population.extend(front)
        else:
            crowding_distances = crowding_distance_assignment(objectives, front)
            sorted_indices = np.argsort(crowding_distances)[::-1]
            next_population.extend(front[sorted_indices[:population_size - len(next_population)]])
            break
    return next_population

# 8. NSGA-II 主算法
for generation in range(num_generations):
    # 计算种群的目标函数值
    f1_values = objective_1(population)
    f2_values = objective_2(population)
    objectives = np.column_stack((f1_values, f2_values))

    # 非支配排序
    fronts = non_dominated_sorting(objectives)

    # 选择下一代种群
    selected_indices = nsga_ii_selection(population, objectives, fronts)
    population = population[selected_indices]

    # 模拟交叉和变异（为了简化，这里随机生成新解）
    population = np.random.uniform(-10, 10, population_size)

# 9. 最后绘制帕累托前沿，并应用自定义字体
f1_values = objective_1(population)
f2_values = objective_2(population)

plt.figure(figsize=(8, 6))
plt.scatter(f1_values, f2_values, label="帕累托前沿", color="blue")
plt.xlabel("目标 1: $f_1(x) = x^2$", fontproperties=custom_font)
plt.ylabel("目标 2: $f_2(x) = (x-2)^2$", fontproperties=custom_font)
plt.title("NSGA-II 结果", fontproperties=custom_font)
plt.legend(prop=custom_font)
plt.grid(True)
plt.show()
