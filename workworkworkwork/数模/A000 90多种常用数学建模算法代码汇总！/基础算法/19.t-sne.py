import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 1. 加载鸢尾花数据集
iris = datasets.load_iris()
X = iris.data  # 特征数据（花萼长度、花萼宽度、花瓣长度、花瓣宽度）
y = iris.target  # 类别标签

# 2. 使用 t-SNE 进行降维，将 4 维数据降至 2 维
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X)

# 3. 创建 DataFrame 保存降维结果
df_tsne = pd.DataFrame(data=X_tsne, columns=['Dim1', 'Dim2'])
df_tsne['Target'] = y

# 4. 可视化降维后的数据
plt.figure(figsize=(8, 6))
colors = ['r', 'g', 'b']
for target, color in zip([0, 1, 2], colors):
    indices_to_keep = df_tsne['Target'] == target
    plt.scatter(df_tsne.loc[indices_to_keep, 'Dim1'],
                df_tsne.loc[indices_to_keep, 'Dim2'],
                c=color, s=50)

plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.title('t-SNE 降维后的鸢尾花数据')
plt.legend(iris.target_names)
plt.grid(True)
plt.show()
