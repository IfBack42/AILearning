import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
import shap
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit

# ----------------------
# 数据预处理
# ----------------------
# 读取数据与合并火山数据
df = pd.read_csv("../merged_nmlgb.csv")
volcano_df = pd.DataFrame({'year': [1991, 1980], 'VEI': [6, 5]})  # 示例数据
df = pd.merge(df, volcano_df, on='year', how='left').fillna(0)
df = df[df["year"] >= 1880].reset_index(drop=True)

# 转换为DatetimeIndex
df['date'] = pd.to_datetime(df['year'], format='%Y')  # 新增步骤：创建日期列
df = df.set_index('date')  # 设置日期索引

# 关键特征插值
cols_to_impute = ["avetem", "tot", "ppm", "VEI"]
for col in cols_to_impute:
    df[col] = df[col].interpolate(method='time')  # 现在索引是时间类型，可安全使用time插值

# 恢复年份列（用于后续分析）
df['year'] = df.index.year  # 新增步骤：从索引中提取年份

# 特征工程
df["co2_5y_ma"] = df["ppm"].rolling(5).mean()
df["volcano_impact"] = (df["VEI"] >= 5).astype(int).shift(1)
df = df.dropna()

# ----------------------
# 模型训练
# ----------------------
features = ["tot", "ppm", "co2_5y_ma", "volcano_impact"]
target = "avetem"

# 标准化
scaler = StandardScaler()
X = scaler.fit_transform(df[features])
y = df[target]

# 训练模型
model = xgb.XGBRegressor(max_depth=3, reg_alpha=1.0, n_estimators=200)
model.fit(X, y)

# 计算SHAP值
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# ----------------------
# 可视化
# ----------------------
plt.rcParams["font.sans-serif"] = ["SimSun"]
fig = plt.figure(figsize=(18, 12))

# 1. 太阳黑子与温度对比（双Y轴）
ax1 = plt.subplot(3, 2, 1)
ax1.plot(df["year"], df["tot"], color="tab:blue", label="太阳黑子数")
ax1.set_ylabel("太阳黑子数", color="tab:blue")
ax2 = ax1.twinx()
ax2.plot(df["year"], df["avetem"], color="tab:red", label="全球温度")
ax2.set_ylabel("温度 (°C)", color="tab:red")
ax1.set_title("太阳黑子数与温度时间序列对比")

# 2. 滞后效应示意图
ax3 = plt.subplot(3, 2, 2)
lags = range(1, 6)
corr = [df["avetem"].corr(df["tot"].shift(lag)) for lag in lags]
ax3.bar(lags, corr, color="skyblue")
ax3.set_xlabel("滞后年数")
ax3.set_ylabel("相关系数")
ax3.set_title("太阳黑子数滞后效应")

# 3. CO₂与温度的SHAP依赖图
ax4 = plt.subplot(3, 2, 3)
shap.dependence_plot("ppm", shap_values, X, feature_names=features,
                     interaction_index=None, ax=ax4, show=False)
ax4.set_title("CO₂浓度与温度的非线性关系")

# 4. SHAP特征重要性
ax5 = plt.subplot(3, 2, 4)
shap.summary_plot(shap_values, X, feature_names=features, plot_type="bar", show=False)
ax5.set_title("SHAP特征重要性")

# 5. 预测值 vs 真实值
ax6 = plt.subplot(3, 1, 3)
df["pred"] = model.predict(X)
ax6.plot(df["year"], df["avetem"], label="实际温度")
ax6.plot(df["year"], df["pred"], linestyle="--", label="预测温度")
ax6.legend()
ax6.set_title("预测值与实际值对比")

plt.tight_layout()
plt.show()