import numpy as np
import pandas as pd

# 定义主观判断矩阵
def subjective_judgement_matrix(size, matrix_name=""):
    matrix = np.ones((size, size))
    for i in range(size):
        for j in range(i+1, size):
            value = float(input(f"请输入 {matrix_name} 第 {i+1} 项与第 {j+1} 项的比较值: "))
            matrix[i, j] = value
            matrix[j, i] = 1 / value
    return matrix

# 计算权重向量
def compute_weights(matrix):
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_eigval = np.max(eigvals)
    eigvec = eigvecs[:, np.argmax(eigvals)]
    weights = np.real(eigvec / np.sum(eigvec))
    return weights, max_eigval

# 一致性检验
def consistency_ratio(matrix, max_eigval):
    n = matrix.shape[0]
    CI = (np.real(max_eigval) - n) / (n - 1)
    RI = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.54, 1.56]
    CR = CI / RI[n-1]
    return CR

# 综合评价
def overall_evaluation(criteria_weights_vector, criteria_weights):
    alternative_weights_matrix = np.array(list(criteria_weights.values())).T
    overall_scores = np.dot(alternative_weights_matrix, criteria_weights_vector)
    return overall_scores

# 输入方案数量和准则数量
num_alternatives = int(input("请输入方案的数量: "))
num_criteria = int(input("请输入准则的数量: "))

# 输入准则层判断矩阵
print("请输入准则层的判断矩阵:")
criteria_matrix = subjective_judgement_matrix(num_criteria, "准则层")

# 计算准则层的权重向量
criteria_weights_vector, criteria_max_eigval = compute_weights(criteria_matrix)
criteria_CR = consistency_ratio(criteria_matrix, criteria_max_eigval)
if criteria_CR >= 0.1:
    raise ValueError(f"准则层判断矩阵的一致性比率过高: {criteria_CR}")

# 输入各准则下的判断矩阵并计算权重向量
criteria_matrices = {}
criteria_weights = {}
for i in range(num_criteria):
    criteria_name = f"准则{i+1}"
    print(f"请输入 {criteria_name} 的判断矩阵:")
    matrix = subjective_judgement_matrix(num_alternatives, criteria_name)
    weights, max_eigval = compute_weights(matrix)
    CR = consistency_ratio(matrix, max_eigval)
    if CR < 0.1:
        criteria_matrices[criteria_name] = matrix
        criteria_weights[criteria_name] = weights
    else:
        raise ValueError(f"{criteria_name} 的一致性比率过高: {CR}")

# 计算每个方案的综合得分
overall_scores = overall_evaluation(criteria_weights_vector, criteria_weights)

# 输出结果
print("方案得分：", overall_scores)
print("层次决策模型：", criteria_weights_vector)
print("判断矩阵汇总结果：", criteria_matrices)
print("方案层判断矩阵汇总结果：", criteria_weights)

# 显示每个方案在每个指标下的得分
alternative_scores = {criteria: criteria_weights[criteria] for criteria in criteria_weights}
print("每个方案在每个指标下的得分：", alternative_scores)
