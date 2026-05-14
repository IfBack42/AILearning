import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 加载数据
file_path = r'D:\py\LearnPython\data.xlsx'
data = pd.read_excel(file_path)


# 数据标准化
def normalize(df):
    return df / df.max()


# 计算灰色关联度
def grey_relational_coefficient(df, reference=None):
    if reference is None:
        reference = df.max()  # 选取各列的最大值作为参考序列
    n_samples, n_features = df.shape
    df_normalized = normalize(df)
    reference_normalized = normalize(reference)

    # 计算关联度
    xi = df_normalized.to_numpy()
    xr = reference_normalized.to_numpy()
    xi_minus_xr = np.abs(xi - xr)

    rho = 0.5  # 分辨系数，通常取值为0.5
    delta_min = np.min(xi_minus_xr)
    delta_max = np.max(xi_minus_xr)

    GR = (delta_min + rho * delta_max) / (xi_minus_xr + rho * delta_max)
    GR_mean = np.mean(GR, axis=1)
    return GR_mean


# 执行灰色关联分析
gra_scores = grey_relational_coefficient(data)

# 添加灰色关联分析得分到原始数据
data['GRA_Score'] = gra_scores

# 可视化灰色关联分析得分
plt.figure(figsize=(10, 6))
plt.bar(data.index, data['GRA_Score'], color='lightgreen')
plt.xlabel('Sample Index')
plt.ylabel('GRA Score')
plt.title('Grey Relational Analysis Scores of Samples')
plt.show()

# 保存结果
output_path = r'D:\py\LearnPython\scored_data_with_gra.xlsx'
data.to_excel(output_path, index=False)
print("数据已处理并保存至:", output_path)
