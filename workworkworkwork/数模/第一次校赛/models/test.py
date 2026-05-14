import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time  # 新增时间模块
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score  # 新增R方模块

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# 1. 增强特征工程
def create_features(df):
    """创建时间序列相关特征"""
    # 基础转换
    df['CO2_log'] = np.log1p(df['CO2'])
    df['Year_poly'] = ((df['Year'] - 1880) / 100) ** 2

    # 动态变化特征
    for window in [3, 5, 10]:
        df[f'CO2_ma{window}'] = df['CO2'].rolling(window, min_periods=1).mean()
        df[f'Temp_ma{window}'] = df['OceanTemp'].rolling(window, min_periods=1).mean()
        df[f'CO2_growth{window}'] = df['CO2'].pct_change(window).fillna(0)

    # 交互特征
    df['CO2_Temp_interact'] = df['CO2_log'] * df['Temp_ma5']
    df['Year_CO2_interact'] = df['Year_poly'] * df['CO2_ma10']

    # 滞后特征（关键修复：使用前向填充）
    for lag in [1, 2, 3]:
        df[f'Temp_lag{lag}'] = df['OceanTemp'].shift(lag).fillna(method='ffill')
        df[f'CO2_lag{lag}'] = df['CO2'].shift(lag).fillna(method='ffill')

    return df


# 2. 数据加载优化
def load_data():
    # 加载并转换数据
    hist = pd.read_csv('../data/historical_data.csv')
    future = pd.read_csv('../data/LSAT_future_features.csv').rename(columns={'year': 'Year'})

    # 划分测试集（2010-2023）
    test_mask = (hist['Year'] >= 2010) & (hist['Year'] <= 2023)
    test = hist[test_mask].copy()
    hist = hist[~test_mask].copy()

    # 合并数据用于特征工程
    full_df = pd.concat([hist, test, future]).reset_index(drop=True)
    full_df = create_features(full_df)

    # 拆分数据集（保留原始索引）
    hist = full_df[full_df['Year'] <= 2009].copy().reset_index(drop=True)
    test = full_df[(full_df['Year'] >= 2010) & (full_df['Year'] <= 2023)].copy().reset_index(drop=True)
    future = full_df[full_df['Year'] >= 2030].copy().reset_index(drop=True)

    return hist, test, future


# 3. 预处理优化
def preprocess(hist, test, future):
    # 特征选择
    features = ['CO2_log', 'OceanTemp', 'Year_poly',
                'CO2_ma5', 'Temp_ma5', 'CO2_growth5',
                'CO2_Temp_interact', 'Year_CO2_interact',
                'Temp_lag1', 'Temp_lag2']

    # 构建预处理管道
    preprocessor = ColumnTransformer([
        ('scaler', RobustScaler(), ['CO2_log', 'OceanTemp', 'CO2_ma5', 'Temp_ma5']),
        ('pass', 'passthrough', ['Year_poly', 'CO2_growth5', 'CO2_Temp_interact', 'Year_CO2_interact'])
    ])

    # 训练预处理器（仅使用历史数据）
    preprocessor.fit(hist[features])

    # 转换数据
    X_train = preprocessor.transform(hist[features])
    X_test = preprocessor.transform(test[features])
    X_future = preprocessor.transform(future[features])

    return X_train, hist.AvgTemp.values, X_test, test.AvgTemp.values, X_future


# 4. 模型训练增强（新增时间记录和R方计算）
def train_predict(X_train, y_train, X_test, y_test, X_future):
    model = GradientBoostingRegressor(
        n_estimators=3000,
        learning_rate=0.02,
        max_depth=25,
        min_samples_split=5,
        max_features=0.6,
        random_state=42,
        subsample=0.8
    )

    # 记录训练时间
    start_train = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_train

    # 记录测试集预测时间
    start_test = time.time()
    y_pred = model.predict(X_test)
    test_time = time.time() - start_test

    # 评估指标
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)  # 新增R方计算

    print(f"\n=== 测试集评估结果（2010-2023）===")
    print(f"MSE: {mse:.3f}")
    print(f"MAE: {mae:.3f} ℃")
    print(f"R²: {r2:.3f}")  # 输出R方
    print(f"训练耗时: {train_time:.2f}秒")
    print(f"测试集预测耗时: {test_time:.4f}秒")

    # 残差诊断图
    residuals = y_test - y_pred
    plt.figure(figsize=(14, 5))

    # 散点图
    plt.subplot(1, 2, 1)
    plt.scatter(y_pred, residuals, alpha=0.6, c='#9467bd', edgecolors='w')
    plt.axhline(0, color='#2ca02c', linestyle='--', linewidth=1.5)
    plt.title('残差散点图（2010-2023）')
    plt.xlabel('预测温度 (°C)')
    plt.ylabel('残差（真实值 - 预测值）')
    plt.grid(alpha=0.3)

    # 分布直方图
    plt.subplot(1, 2, 2)
    plt.hist(residuals, bins=15, color='#9467bd', edgecolor='w', alpha=0.7)
    plt.axvline(0, color='#2ca02c', linestyle='--', linewidth=1.5)
    plt.title('残差分布直方图')
    plt.xlabel('残差值')
    plt.ylabel('频数')

    plt.tight_layout()
    plt.show()

    # 记录未来预测时间
    start_future = time.time()
    future_preds = model.predict(X_future)
    future_time = time.time() - start_future
    print(f"未来预测耗时: {future_time:.4f}秒")

    return future_preds


# 5. 主程序（保持其他逻辑不变）
def main():
    # 数据流程
    hist, test, future = load_data()
    X_train, y_train, X_test, y_test, X_future = preprocess(hist, test, future)

    # 训练预测
    preds = train_predict(X_train, y_train, X_test, y_test, X_future)

    # 生成结果（使用iloc安全访问）
    base_temp = hist.AvgTemp.iloc[-1]
    preds = np.clip(preds, base_temp * 0.98, base_temp * 1.15)

    # 趋势增强处理（仅影响未来预测）
    trend_factor = np.linspace(0, 1.5, len(preds))
    preds = preds * (1 + trend_factor * 0.025)

    # 后处理保证单调性
    preds = np.maximum.accumulate(preds)
    result = pd.DataFrame({
        'Year': future.Year,
        '预测温度': np.round(preds, 2),
        '趋势强度': np.round(trend_factor, 2)
    })

    # 高级可视化（三阶段对比）
    plt.figure(figsize=(14, 7))
    plt.plot(hist.Year, hist.AvgTemp, '#1f77b4', lw=2, label='历史观测')
    plt.plot(test.Year, y_test, '#ff7f0e', lw=2, label='测试集真实值')
    plt.plot(result.Year, result.预测温度, '#d62728', lw=1.5, label='预测趋势')
    plt.title('全球平均气温预测趋势 (2030-2050)', fontsize=14)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('温度 (°C)', fontsize=12)
    plt.axvline(2030, color='#2ca02c', ls='--', label='预测起点')
    plt.grid(alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return result


if __name__ == "__main__":
    df = main()
    print("\n=== 最终预测结果 ===")
    print(df[['Year', '预测温度']].to_string(index=False))