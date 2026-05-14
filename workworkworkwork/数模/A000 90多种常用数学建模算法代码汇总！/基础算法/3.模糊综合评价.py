import numpy as np


def fuzzy_comprehensive_evaluation():
    # 输入方案个数和指标个数
    num_schemes = int(input("请输入方案的个数: "))
    num_indicators = int(input("请输入每个方案的指标个数: "))

    # 输入隶属度矩阵
    print("请输入每个方案对应每个指标的隶属度:")
    membership_matrix = []
    for i in range(num_schemes):
        row = list(map(float, input(f"请输入第{i + 1}个方案的隶属度，以空格分隔: ").split()))
        membership_matrix.append(row)

    # 转换为numpy数组
    R = np.array(membership_matrix)

    # 输入权重向量
    weight_vector = list(map(float, input("请输入权重向量，以空格分隔: ").split()))
    A = np.array(weight_vector)

    # 进行模糊综合运算
    # R的每一列都是一个指标的隶属度，因此应该进行按列加权平均
    B = np.dot(R, A.T)

    # 返回最终评价结果
    print("模糊综合评价结果为: ", B)


# 调用函数
fuzzy_comprehensive_evaluation()

