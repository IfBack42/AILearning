# -*- coding: utf-8 -*-
"""
完整的气候变化分析模型（集成特征工程、XGBoost建模、可解释性分析）
数据要求：包含年份、气候指标的CSV文件
"""

# =====================
# 环境配置
# =====================
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import shap

# 中文显示配置
plt.rcParams["font.sans-serif"] = ["SimSun"]
plt.rcParams["axes.unicode_minus"] = False


# =====================
# 数据准备
# =====================
def load_data():
    """加载并整合多源数据"""
    # 读取基础数据
    df = pd.read_csv("../merged_nmlgb.csv")

    # 火山爆发数据（示例数据）
    volcano_data = {
        'year': [
            1912, 1921, 1935, 1941, 1943, 1944, 1946, 1951, 1956, 1963, 1964, 1972,
            1974, 1975, 1976, 1977, 1980, 1982, 1984, 1985, 1986, 1987, 1988, 1991,
            1991, 1995, 1996, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
            2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
        ],
        'VEI': [
            6, 3, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6
        ]
    }

    # 数据合并与清洗
    volcano_df = pd.DataFrame(volcano_data)
    df = pd.merge(df, volcano_df, on='year', how='left').fillna({'VEI': 0})

    # 时间序列处理
    df = df[df["year"] >= 1880].reset_index(drop=True)
    df['date'] = pd.to_datetime(df['year'], format='%Y')
    return df.set_index('date')


# =====================
# 特征工程
# =====================
def feature_engineering(df):
    """高级特征构造"""
    # 时间序列插值
    cols_to_impute = ["avetem", "ppb", "burnt_area", "tree_loss", "SO2", "ppm", "VEI"]
    df[cols_to_impute] = df[cols_to_impute].interpolate(method='time', limit_direction='both')

    # 滞后特征
    df["burnt_area_lag3"] = df["burnt_area"].shift(3)
    df["burnt_3y_avg"] = df["burnt_area"].rolling(3, min_periods=1).mean()

    # 火山特征
    df["volcano_effect"] = np.where(df["VEI"] >= 5, 1, 0)
    df["post_volcano"] = df["volcano_effect"].shift(1).rolling(3).max()

    # 交互特征
    df["co2_wildfire"] = df["ppm"] * df["burnt_area_lag3"]

    # 气候指数（示例数据）
    np.random.seed(42)
    df["ENSO_index"] = np.random.normal(0, 1, len(df))

    return df.reset_index().dropna()


# =====================
# 建模训练
# =====================
def train_model(X, y):
    """时间序列交叉验证训练"""
    tscv = TimeSeriesSplit(n_splits=5)
    model_params = {
        'objective': 'reg:squarederror',
        'n_estimators': 800,
        'max_depth': 4,
        'learning_rate': 0.05,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'reg_alpha': 0.2,
        'reg_lambda': 0.2,
        'random_state': 42
    }

    scores = []
    for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model = xgb.XGBRegressor(**model_params)
        model.fit(X_train, y_train)

        pred = model.predict(X_test)
        scores.append({
            'fold': fold + 1,
            'mse': mean_squared_error(y_test, pred),
            'r2': r2_score(y_test, pred)
        })

    # 全量训练
    final_model = xgb.XGBRegressor(**model_params).fit(X, y)
    return pd.DataFrame(scores), final_model


# =====================
# 可视化模块
# =====================
def visualize_results(df, model, X_scaled, features):
    """生成全套分析图表"""
    # 特征重要性
    importance = model.feature_importances_
    feat_imp = pd.DataFrame({"Feature": features, "Importance": importance}) \
        .sort_values("Importance", ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x="Importance", y="Feature", data=feat_imp, palette="viridis")
    plt.title("优化后特征重要性分析")
    plt.tight_layout()

    # 预测趋势对比
    df["prediction"] = model.predict(X_scaled)
    plt.figure(figsize=(14, 6))
    plt.plot(df["year"], df["avetem"], label="实际温度", linewidth=2)
    plt.plot(df["year"], df["prediction"], label="预测温度", linestyle="--")
    plt.xlabel("年份")
    plt.ylabel("全球均温 (°C)")
    plt.title("全球温度预测效果对比")
    plt.legend()
    plt.grid(True)

    # SHAP分析
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_scaled)

    # CO₂依赖图
    plt.figure(figsize=(10, 6))
    shap.dependence_plot(
        features.index("ppm"),
        shap_values,
        X_scaled,
        feature_names=features,
        display_features=df[features].values,
        show=False
    )
    plt.axvline(x=410, color='#FF4500', linestyle='--', linewidth=2, alpha=0.8)
    plt.title("CO₂浓度与温度响应的非线性关系")
    plt.xlabel("CO₂浓度 (ppm)")
    plt.ylabel("SHAP值（温度影响程度）")

    # 显示所有图表
    plt.show()


# =====================
# 主程序
# =====================
if __name__ == "__main__":
    # 数据管道
    df = load_data()
    df = feature_engineering(df)

    # 特征选择
    features = [
        "ppm", "ppb", "tot", "SO2", "burnt_area_lag3",
        "burnt_3y_avg", "post_volcano", "co2_wildfire", "ENSO_index"
    ]
    target = "avetem"

    X = df[features]
    y = df[target]

    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 模型训练
    score_df, final_model = train_model(X_scaled, y)
    print("\n=== 交叉验证结果 ===")
    print(score_df)
    print(f"\n平均 MSE: {score_df.mse.mean():.4f} (±{score_df.mse.std():.4f})")
    print(f"平均 R²: {score_df.r2.mean():.4f} (±{score_df.r2.std():.4f})")

    # 可视化分析
    visualize_results(df, final_model, X_scaled, features)