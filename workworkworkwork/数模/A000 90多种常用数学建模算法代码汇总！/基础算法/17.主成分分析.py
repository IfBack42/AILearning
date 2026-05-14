import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 1. 生成模拟信用评分数据集
# 数据集包含客户的4个特征：年收入、信用卡余额、贷款金额和信用评分
np.random.seed(42)
n_samples = 100

# 年收入（单位：美元），随机生成范围 20k 到 100k
income = np.random.randint(20000, 100000, size=n_samples)

# 信用卡余额（单位：美元），随机生成范围 0 到 10k
credit_card_balance = np.random.randint(0, 10000, size=n_samples)

# 贷款金额（单位：美元），随机生成范围 0 到 50k
loan_amount = np.random.randint(0, 50000, size=n_samples)

# 信用评分（范围 300 到 850）
credit_score = np.random.randint(300, 850, size=n_samples)

# 组合成 DataFrame
df = pd.DataFrame({
    'Income': income,
    'Credit Card Balance': credit_card_balance,
    'Loan Amount': loan_amount,
    'Credit Score': credit_score
})

print("原始数据集的前5行：")
print(df.head())

# 2. 数据标准化处理
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# 3. 使用 PCA 进行降维，将 4 维数据降至 2 维
pca = PCA(n_components=2)
df_pca = pca.fit_transform(df_scaled)

# 创建 DataFrame 保存降维结果
df_pca = pd.DataFrame(data=df_pca, columns=['PC1', 'PC2'])

# 4. 分析主成分的重要性
explained_variance = pca.explained_variance_ratio_
print(f"\n主成分1解释的方差比例: {explained_variance[0]:.2f}")
print(f"主成分2解释的方差比例: {explained_variance[1]:.2f}")

# 5. 可视化降维后的数据
plt.figure(figsize=(8, 6))
plt.scatter(df_pca['PC1'], df_pca['PC2'], s=50, edgecolor='k')
plt.xlabel('主成分1 (PC1)')
plt.ylabel('主成分2 (PC2)')
plt.title('信用评分数据的 PCA 降维结果')
plt.grid(True)
plt.show()

# 6. 查看 PCA 的主成分（特征向量）
print("\n主成分（特征向量）：")
print(pca.components_)
