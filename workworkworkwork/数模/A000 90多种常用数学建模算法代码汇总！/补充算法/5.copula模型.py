import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, multivariate_normal

# 1. 设定公司 A 和 B 的违约概率
P_A = 0.05  # 公司 A 的一年违约概率 5%
P_B = 0.07  # 公司 B 的一年违约概率 7%

# 2. 计算对应的标准正态分布下的 quantile (逆CDF)
u_A = norm.ppf(P_A)  # 对应 P_A 的正态分布的分位点
u_B = norm.ppf(P_B)  # 对应 P_B 的正态分布的分位点

# 3. 使用高斯 Copula 模型
def gaussian_copula_joint_default_probability(u_A, u_B, rho):
    """
    使用高斯 Copula 模型计算联合违约概率
    参数:
    - u_A: 公司 A 的分位点 (通过 P_A 计算)
    - u_B: 公司 B 的分位点 (通过 P_B 计算)
    - rho: A 和 B 之间的相关系数
    返回:
    - 联合违约概率
    """
    # 构造协方差矩阵
    cov_matrix = [[1, rho], [rho, 1]]  # 相关系数矩阵
    # 构造二维正态分布，并设置 allow_singular=True 允许奇异矩阵
    mvn = multivariate_normal(mean=[0, 0], cov=cov_matrix, allow_singular=True)
    return mvn.cdf([u_A, u_B])  # 计算联合分布的 CDF

# 4. 计算不同相关系数下的联合违约概率
rhos = np.linspace(-0.99, 0.99, 100)  # 相关系数从 -0.99 到 0.99 的变化，避免极值
joint_default_probabilities = [gaussian_copula_joint_default_probability(u_A, u_B, rho) for rho in rhos]

# 5. 绘制联合违约概率随相关系数变化的曲线
plt.figure(figsize=(10, 6))
plt.plot(rhos, joint_default_probabilities, color='blue')
plt.title("联合违约概率随相关系数的变化", fontsize=14)
plt.xlabel("相关系数 $\\rho$", fontsize=12)
plt.ylabel("联合违约概率", fontsize=12)
plt.grid(True)
plt.show()

# 打印在不同相关系数下的联合违约概率
for rho in [-0.5, 0, 0.5, 0.8]:
    joint_prob = gaussian_copula_joint_default_probability(u_A, u_B, rho)
    print(f"当相关系数 rho = {rho:.1f} 时，两家公司同时违约的概率为 {joint_prob:.4%}")
