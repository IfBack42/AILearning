import numpy as np
import pandas as pd
from sklearn.decomposition import FactorAnalysis
import matplotlib.pyplot as plt

# 1. 生成模拟数据集
np.random.seed(42)
n_samples = 500

# 假设有5个变量：收入、教育水平、工作经验、消费金额、贷款
income = np.random.normal(50000, 15000, size=n_samples)
education = np.random.normal(16, 2, size=n_samples)  # 教育年限
work_experience = np.random.normal(10, 5, size=n_samples)  # 工作年限
spending = np.random.normal(3000, 800, size=n_samples)  # 每月消费
loan = np.random.normal(20000, 5000, size=n_samples)  # 贷款金额

# 将这些变量组合成一个数据集
df = pd.DataFrame({
    'Income': income,
    'Education': education,
    'Work Experience': work_experience,
    'Spending': spending,
    'Loan': loan
})

# 2. 因子分析，假设提取2个因子
fa = FactorAnalysis(n_components=2, random_state=42)
fa.fit(df)

# 3. 提取因子负荷矩阵
factor_loadings = fa.components_.T
print("因子负荷矩阵：")
print(pd.DataFrame(factor_loadings, index=df.columns, columns=['Factor 1', 'Factor 2']))

# 4. 解释主成分贡献率
explained_variance = fa.noise_variance_
print("\n噪声方差（未解释部分）：")
print(explained_variance)

