# 完整整合代码（包含显著性分析）
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats  # 新增库
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import statsmodels.api as sm  # 新增库

plt.rcParams["font.sans-serif"] = ["SimSun"]
plt.rcParams["axes.unicode_minus"] = False

# --------------------------
# 数据预处理（共用部分）
# --------------------------
# 读取数据
df = pd.read_csv('../shabi.csv')

# 处理重复列
df = df.loc[:, ~df.columns.duplicated()]


# 经度格式化函数
def parse_longitude(s):
    if isinstance(s, str):
        s = s.strip()
        val, dir = float(s[:-1]), s[-1]
        return -val if dir == 'W' else val
    return s


# 应用格式化
df['Longitude'] = df['Longitude'].apply(parse_longitude)

# 定义纬度带
latitude_bins = [-90, -60, -30, 0, 30, 60, 90]
latitude_labels = [
    "South High", "South Mid", "South Low",
    "North Low", "North Mid", "North High"
]
df["Latitude Zone"] = pd.cut(
    df["Latitude"],
    bins=latitude_bins,
    labels=latitude_labels,
    ordered=False
)

# --------------------------
# 文档1分析内容
# --------------------------
# 分析1：分面散点图（保持不变）
plt.figure(figsize=(12, 10))
g = sns.FacetGrid(
    df,
    col="Latitude Zone",
    col_wrap=3,
    height=4,
    sharey=False
)
g.map(sns.scatterplot, "Longitude", "AverageTemperature", alpha=0.5)
g.set_axis_labels("Longitude", "Temperature (°C)")
plt.tight_layout()
plt.show()


# ================= 修改点1：带p值的Spearman相关系数 =================
def spearman_with_p(x, features, target):
    """计算带p值的Spearman相关系数"""
    corr_series = pd.Series(dtype=float)
    p_series = pd.Series(dtype=float)

    for col in features:
        if col == target:
            continue
        # 删除缺失值
        valid_data = x[[target, col]].dropna()
        if len(valid_data) < 2:
            corr, p = np.nan, np.nan
        else:
            corr, p = stats.spearmanr(valid_data[target], valid_data[col])
        corr_series[col] = corr
        p_series[col] = p

    return pd.DataFrame({
        'Correlation': corr_series,
        'P-value': p_series
    })


# 分组计算（替换原始分析2）
corr_results = df.groupby("Latitude Zone").apply(
    lambda x: spearman_with_p(
        x,
        features=["Elevation", "Distance_to_Sea_km"],
        target="AverageTemperature"
    )
)

print("\n" + "=" * 60)
print("各纬度带温度与地理因素的Spearman相关系数及p值：")
print(corr_results.round(2))
print("=" * 60 + "\n")

# 分析3：回归趋势图（保持不变）
plt.figure(figsize=(12, 10))
sns.lmplot(
    data=df,
    x="Latitude",
    y="AverageTemperature",
    hue="Latitude Zone",
    ci=None,
    height=6,
    aspect=2.0
)
plt.title("Temperature vs Latitude by Zone")
plt.show()

# --------------------------
# 文档2分析内容
# --------------------------
# 数值型特征定义
numerical_cols = [
    'Latitude', 'Longitude', 'Elevation',
    'Distance_to_Sea_km', 'AverageTemperature'
]

# 散点图矩阵（保持结构）
sns.pairplot(df[numerical_cols])
plt.suptitle(
    'Pairwise Relationships (对角线为分布，散点图展示原始数据)',
    y=1.0
)
plt.show()

# ================= 修改点2：带p值的相关系数矩阵 =================
# 计算相关系数矩阵（新增函数）
corr_matrix = df[numerical_cols].corr(method='spearman')


def calculate_spearman_p(df):
    """生成带p值的相关系数矩阵"""
    cols = df.columns
    n = len(cols)
    p_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                p_matrix[i, j] = 0
                continue
            valid = df.iloc[:, [i, j]].dropna()
            if len(valid) < 2:
                p_matrix[i, j] = np.nan
            else:
                _, p = stats.spearmanr(valid.iloc[:, 0], valid.iloc[:, 1])
                p_matrix[i, j] = p

    return pd.DataFrame(
        p_matrix,
        index=cols,
        columns=cols
    )


# 计算p值矩阵
p_matrix = calculate_spearman_p(df[numerical_cols])

# 绘制带星号标记的热力图（替换原始热力图）
plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
annot_matrix = np.where(
    p_matrix < 0.01, "**",
    np.where(p_matrix < 0.05, "*", "")
).astype(str)

sns.heatmap(
    corr_matrix,
    annot=annot_matrix,  # 显示显著性标记
    fmt="",
    cmap='coolwarm',
    mask=mask,
    vmin=-1,
    vmax=1,
    linewidths=0.5
)
plt.title('Spearman Correlation with Significance (*p<0.05, **p<0.01)')
plt.show()

# ================= 修改点3：带p值的回归分析 =================
# 分类变量编码（需确保存在Latitude_tape列）
le = LabelEncoder()
df['Latitude_tape_encoded'] = le.fit_transform(df['Latitude_tape'])

# 准备数据（使用statsmodels）
X = df[[
    'Latitude', 'Longitude', 'Elevation',
    'Distance_to_Sea_km', 'Latitude_tape_encoded'
]]
y = df['AverageTemperature']
X = sm.add_constant(X)  # 添加截距项

# 执行OLS回归（替换原始回归分析）
model = sm.OLS(y, X).fit()

# 提取结果
results_df = pd.DataFrame({
    'Feature': model.params.index,
    'Coefficient': model.params.values,
    'P-value': model.pvalues.values
})

# 添加显著性标记
results_df['Significance'] = np.select(
    [
        results_df['P-value'] < 0.001,
        results_df['P-value'] < 0.01,
        results_df['P-value'] < 0.05,
        results_df['P-value'] < 0.1
    ],
    ['***', '**', '*', '.'],
    default=''
)

print("\n" + "=" * 60)
print("线性回归系数及显著性：")
print(results_df.round(2))
print("显著性标记：*** p<0.001, ** p<0.01, * p<0.05, . p<0.1")
print("=" * 60)