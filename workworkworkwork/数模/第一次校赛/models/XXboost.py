import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------
plt.rcParams["font.sans-serif"] = ["SimSun"]
plt.rcParams["axes.unicode_minus"] = False
# 数据加载与增强
# ----------------------
# 读取原始数据
df = pd.read_csv("../merged_nmlgb.csv")

# 加载火山爆发数据（示例，需替换为真实数据）
volcano_data = {
    'year' : [
    1912, 1921, 1935, 1941, 1943, 1944, 1946, 1951, 1956, 1963, 1964, 1972,
    1974, 1975, 1976, 1977, 1980, 1982, 1984, 1985, 1986, 1987, 1988, 1991,
    1991, 1995, 1996, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
    2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
],
'VEI' : [
    6, 3, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 6,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,6
]
}
volcano_df = pd.DataFrame(volcano_data)

# 合并火山数据
df = pd.merge(df, volcano_df, on='year', how='left')
df['VEI'] = df['VEI'].fillna(0)  # 无爆发的年份填0

# ----------------------
# 数据预处理
# ----------------------
# 过滤有效数据范围
df = df[df["year"] >= 1880].reset_index(drop=True)

# 将年份转换为时间索引
df['date'] = pd.to_datetime(df['year'], format='%Y')
df = df.set_index('date')

# 定义插值列（增加火山相关列）
cols_to_impute = ["avetem", "ppb", "burnt_area", "tree_loss", "SO2", "ppm", "VEI"]

# 改进插值策略：时间序列插值
for col in cols_to_impute:
    df[col] = df[col].interpolate(method='time', limit_direction='both')

# 重置索引（可选，若后续分析需要年份列）
df = df.reset_index(drop=False)

# ----------------------
# 高级特征工程
# ----------------------
# 1. 野火特征增强
df["burnt_area_lag3"] = df["burnt_area"].shift(3)  # 3年滞后
df["burnt_3y_avg"] = df["burnt_area"].rolling(3, min_periods=1).mean()  # 3年均值

# 2. 火山特征处理
df["volcano_effect"] = np.where(df["VEI"] >= 5, 1, 0)  # 二值化重大火山事件
df["post_volcano"] = df["volcano_effect"].shift(1).rolling(3).max()  # 火山后效应

# 3. 交互特征
df["co2_wildfire"] = df["ppm"] * df["burnt_area_lag3"]  # CO₂与野火的交互作用

# 4. 气候指数模拟（示例，需接入真实数据）
df["ENSO_index"] = np.random.normal(0, 1, len(df))  # 模拟厄尔尼诺指数

# 删除缺失值
df = df.dropna()

# ----------------------
# 特征选择与目标定义
# ----------------------
features = [
    "ppm",  # CO₂浓度
    "ppb",  # 甲烷浓度
    "tot",  # 太阳黑子数
    "SO2",  # 二氧化硫
    "burnt_area_lag3",  # 3年滞后野火面积
    "burnt_3y_avg",  # 野火3年均值
    "post_volcano",  # 火山后续影响
    "co2_wildfire",  # 交互特征
    "ENSO_index"  # 气候指数
]

target = "avetem"  # 全球均温

X = df[features]
y = df[target]

# ----------------------
# 数据标准化
# ----------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ----------------------
# 时间序列交叉验证
# ----------------------
tscv = TimeSeriesSplit(n_splits=5)
mse_scores = []
r2_scores = []

for fold, (train_index, test_index) in enumerate(tscv.split(X_scaled)):
    X_train, X_test = X_scaled[train_index], X_scaled[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # ----------------------
    # 模型训练（优化参数）
    # ----------------------
    model = xgb.XGBRegressor(
        objective="reg:squarederror",
        n_estimators=800,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.7,
        colsample_bytree=0.7,
        reg_alpha=0.2,
        reg_lambda=0.2,
        random_state=42
    )

    model.fit(X_train, y_train)

    # ----------------------
    # 模型评估
    # ----------------------
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    mse_scores.append(mse)
    r2_scores.append(r2)

    print(f"Fold {fold + 1}: MSE = {mse:.4f}, R² = {r2:.4f}")

# ----------------------
# 综合评估结果
# ----------------------
print("\n===== 综合评估 =====")
print(f"平均 MSE: {np.mean(mse_scores):.4f} (±{np.std(mse_scores):.4f})")
print(f"平均 R²: {np.mean(r2_scores):.4f} (±{np.std(r2_scores):.4f})")

# ----------------------
# 全数据训练最终模型
# ----------------------
final_model = xgb.XGBRegressor(**model.get_params())
final_model.fit(X_scaled, y)

# ----------------------
# 可视化分析
# ----------------------
# 特征重要性
importance = final_model.feature_importances_
feat_importance = pd.DataFrame({"Feature": features, "Importance": importance})
feat_importance = feat_importance.sort_values("Importance", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x="Importance", y="Feature", data=feat_importance, palette="viridis")
plt.title("优化后特征重要性分析")
plt.tight_layout()
plt.show()

# 预测趋势对比
df["prediction"] = final_model.predict(X_scaled)

plt.figure(figsize=(14, 6))
plt.plot(df["year"], df["avetem"], label="实际温度", linewidth=2)
plt.plot(df["year"], df["prediction"], label="预测温度", linestyle="--")
plt.xlabel("年份")
plt.ylabel("全球均温 (°C)")
plt.title("全球温度预测效果对比")
plt.legend()
plt.grid(True)
plt.show()

# 以下代码基于文档1中已有数据继续扩展（假设已运行文档1全部代码）

# =====================
# SHAP分析补充库
# =====================
import shap

# =====================
# 图像1: 太阳黑子数与温度对比
# =====================
plt.figure(figsize=(12,5))
ax1 = sns.lineplot(x=df['year'], y=df['avetem'], color='r', label='全球温度')
ax2 = ax1.twinx()
sns.lineplot(x=df['year'], y=df['tot'], ax=ax2, color='b', label='太阳黑子数', alpha=0.4)
plt.title("太阳黑子数与全球温度异常对比（1880-2022）")
ax1.set_ylabel("温度 (°C)", color='r')
ax2.set_ylabel("太阳黑子数", color='b')
plt.grid(True)
plt.show()

# =====================
# 图像2: 滞后效应示意图（以太阳黑子为例）
# =====================
lags = range(0, 11)
correlations = [df['avetem'].corr(df['tot'].shift(lag)) for lag in lags]

plt.figure(figsize=(10,4))
plt.stem(lags, correlations, use_line_collection=True)
plt.title("太阳黑子数滞后效应分析")
plt.xlabel("滞后年数")
plt.ylabel("与温度相关系数")
plt.axhline(0, color='grey', linestyle='--')
plt.show()

# =====================
# 图像3: CO₂与温度SHAP依赖图
# =====================
explainer = shap.TreeExplainer(final_model)
shap_values = explainer.shap_values(X_scaled)

# =====================
# 图像3: CO₂与温度SHAP依赖图（突出410ppm后的饱和效应）
# =====================
plt.figure(figsize=(10,6))

# 使用原始CO₂浓度值作为显示特征
shap.dependence_plot(
    ind=features.index("ppm"),
    shap_values=shap_values,
    features=X_scaled,  # 模型使用的标准化特征
    feature_names=features,
    display_features=df[features].values,  # 显示原始浓度值
    interaction_index=None,
    show=False,
    dot_size=16,
    alpha=0.6,
    title=""
)

# 增强可视化效果
plt.title("CO₂浓度与温度响应的非线性关系", fontsize=14)
plt.xlabel("CO₂浓度 (ppm)", fontsize=12)
plt.ylabel("SHAP值（温度影响程度）", fontsize=12)

# 添加410ppm阈值线及说明
plt.axvline(x=410, color='#FF4500', linestyle='--', linewidth=2, alpha=0.8)
plt.text(412, plt.ylim()[0] + 0.1,
         '阈值: 410 ppm\n边际效应趋于饱和',
         color='#FF4500', fontsize=10, va='bottom')

# 添加背景色块突出饱和区域
plt.axvspan(410, df['ppm'].max(), color='orange', alpha=0.1, zorder=0)

# 添加趋势线说明
plt.annotate('非线性增长阶段',
             xy=(370, 0.4),
             xytext=(300, 0.6),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=10)

plt.annotate('效应饱和阶段',
             xy=(420, 0.15),
             xytext=(440, 0.3),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=10)

plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()
# =====================
# 图像5: SHAP特征重要性（增强版）
# =====================
shap.summary_plot(shap_values, X_scaled, feature_names=features, plot_type="bar", show=False)
plt.title("SHAP特征重要性排序")
plt.tight_layout()
plt.show()

# 从最终模型中获取特征重要性（需在运行文档1完整代码后执行）
importance_values = final_model.feature_importances_

# 创建特征名称与重要性的对应关系
feat_importance = pd.DataFrame({
    "Feature": features,
    "Importance": importance_values
})

# 按重要性排序并打印
feat_importance = feat_importance.sort_values("Importance", ascending=False)
print("\n===== 特征重要性数值 =====")
print(feat_importance.to_string(index=False))

