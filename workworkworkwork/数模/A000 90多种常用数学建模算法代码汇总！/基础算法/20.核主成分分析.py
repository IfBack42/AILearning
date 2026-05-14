import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import StandardScaler

# 1. 加载鸢尾花数据集
iris = datasets.load_iris()
X = iris.data  # 特征数据
y = iris.target  # 类别标签

# 2. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. 应用核 PCA，使用高斯核（RBF 核）
kpca = KernelPCA(n_components=2, kernel='rbf', gamma=0.1)
X_kpca = kpca.fit_transform(X_scaled)

# 4. 创建 DataFrame 保存降维结果
df_kpca = pd.DataFrame(data=X_kpca, columns=['Principal Component 1', 'Principal Component 2'])
df_kpca['Target'] = y

# 5. 可视化降维后的数据
plt.figure(figsize=(8, 6))
colors = ['r', 'g', 'b']
for target, color in zip([0, 1, 2], colors):
    indices_to_keep = df_kpca['Target'] == target
    plt.scatter(df_kpca.loc[indices_to_keep, 'Principal Component 1'],
                df_kpca.loc[indices_to_keep, 'Principal Component 2'],
                c=color, s=50)

plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Kernel PCA of Iris Dataset')
plt.legend(iris.target_names)
plt.grid(True)
plt.show()
