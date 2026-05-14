import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

FEATURES = ['Year', 'CO2', 'OceanTemp']


# 1. 数据加载与处理
def load_data():
    hist = pd.read_csv('../data/historical_data.csv')
    future = pd.read_csv('../data/LSAT_future_features.csv').rename(columns={'year': 'Year'})

    # 划分测试集（2010-2023）
    test_mask = (hist['Year'] >= 2010) & (hist['Year'] <= 2023)
    test = hist[test_mask].copy()
    hist = hist[~test_mask].copy()

    return hist, test, future[FEATURES]


# 2. 预处理优化
def preprocess(hist, test, future):
    # 合并历史+未来数据用于标准化
    full_features = pd.concat([hist[FEATURES], test[FEATURES], future])

    # 添加时序特征
    full_features['Year_norm'] = (full_features['Year'] - 1880) / 100

    # 标准化器训练（仅用历史数据）
    scaler = StandardScaler()
    scaler.fit(full_features[:len(hist)])

    # 转换所有数据集
    X_train = scaler.transform(full_features[:len(hist)])
    X_test = scaler.transform(full_features[len(hist):len(hist) + len(test)])
    X_future = scaler.transform(full_features[len(hist) + len(test):])

    return X_train, hist['AvgTemp'], X_test, test['AvgTemp'], X_future


# 3. 模型构建（保持原参数）
def build_model():
    return RandomForestRegressor(
        n_estimators=1500,
        max_depth=30,
        min_samples_split=3,
        max_features=0.9,
        random_state=42,
        n_jobs=-1
    )


# 4. 主程序增强
def main():
    # 加载数据
    hist, test, future = load_data()

    # 预处理
    X_train, y_train, X_test, y_test, X_future = preprocess(hist, test, future)

    # 训练模型
    model = build_model()
    model.fit(X_train, y_train)

    # 测试集预测
    y_pred = model.predict(X_test)

    # 评估指标
    print(f"\n测试集评估结果（2010-2023）:")
    print(f"MSE: {mean_squared_error(y_test, y_pred):.3f}")
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.3f} ℃")

    # 残差图
    plt.figure(figsize=(10, 5))
    residuals = y_test - y_pred
    plt.scatter(y_pred, residuals, alpha=0.6, c='purple', edgecolors='w')
    plt.axhline(0, color='r', linestyle='--', linewidth=1)
    plt.title('测试集残差分布（2010-2023）')
    plt.xlabel('预测温度 (°C)')
    plt.ylabel('残差（真实值 - 预测值）')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # 未来预测
    future_preds = model.predict(X_future)

    # 趋势修正（仅应用未来预测）
    base_temp = y_train.iloc[-1]
    trend = np.linspace(0, 2.5, len(future_preds))
    future_preds = future_preds + trend * (future_preds - base_temp) * 0.1

    # 结果生成
    result = pd.DataFrame({
        'Year': future['Year'],
        'PredictedTemp': np.round(future_preds, 2)
    })

    # 可视化
    plt.figure(figsize=(12, 6))
    plt.plot(hist['Year'], hist['AvgTemp'], label='历史观测')
    plt.plot(test['Year'], y_test, 'g-', label='测试集真实值')
    plt.plot(result['Year'], result['PredictedTemp'], 'r--', label='预测趋势')
    plt.title('全球气温预测 (2030-2050)')
    plt.xlabel('年份')
    plt.ylabel('温度 (°C)')
    plt.axvline(2030, color='gray', ls='--')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()

    return result


if __name__ == "__main__":
    df = main()
    print("\n预测结果：")
    print(df.to_string(index=False))