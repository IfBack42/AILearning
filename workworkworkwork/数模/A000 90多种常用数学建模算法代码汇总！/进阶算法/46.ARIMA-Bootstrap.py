# 导入必要的库
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.utils import resample
from statsmodels.tsa.stattools import adfuller, acf, pacf

# 1. 生成更复杂的模拟时间序列数据
np.random.seed(42)
n_samples = 300  # 样本数量
time = np.arange(n_samples)
# 生成带有趋势、季节性成分和更复杂的噪声的时间序列数据
trend = 0.03 * time + np.random.normal(0, 0.5, n_samples)
seasonality = 15 * np.sin(2 * np.pi * time / 30)  # 周期为30
noise = np.random.normal(0, 2, n_samples)
time_series = trend + seasonality + noise

# 将时间序列数据转换为 pandas DataFrame
data = pd.DataFrame({'time_series': time_series})

# 2. 拆分训练集和测试集
train_size = int(len(time_series) * 0.8)
train, test = time_series[:train_size], time_series[train_size:]

# 3. 使用AIC自动选择最佳ARIMA模型参数
def best_arima_model(train):
    best_aic = np.inf
    best_order = None
    best_model = None
    # 遍历不同的p, d, q组合
    for p in range(1, 6):
        for d in range(0, 2):
            for q in range(1, 6):
                try:
                    model = ARIMA(train, order=(p, d, q))
                    result = model.fit()
                    if result.aic < best_aic:
                        best_aic = result.aic
                        best_order = (p, d, q)
                        best_model = result
                except:
                    continue
    return best_model, best_order

# 选择最佳ARIMA模型
arima_model, best_order = best_arima_model(train)
print(f"选择的ARIMA模型参数为: {best_order}")

# 4. 预测残差
residuals = arima_model.resid  # 获取残差
forecast_steps = len(test)  # 预测步数

# 5. Bootstrap 重采样残差
n_bootstrap = 2000  # 重采样次数
bootstrap_forecasts = np.zeros((n_bootstrap, forecast_steps))

# 开始重采样并生成预测路径
for i in range(n_bootstrap):
    resampled_residuals = resample(residuals, replace=True, n_samples=forecast_steps)
    # 预测未来的值，并加上 Bootstrap 残差
    forecast = arima_model.forecast(steps=forecast_steps) + resampled_residuals
    bootstrap_forecasts[i, :] = forecast

# 6. 计算平均预测值和95%置信区间
mean_forecast = np.mean(bootstrap_forecasts, axis=0)
conf_interval_lower = np.percentile(bootstrap_forecasts, 2.5, axis=0)
conf_interval_upper = np.percentile(bootstrap_forecasts, 97.5, axis=0)

# 7. 可视化预测结果
plt.figure(figsize=(12, 6))
plt.plot(np.arange(len(train), len(time_series)), test, label='真实值', color='blue')
plt.plot(np.arange(len(train), len(time_series)), mean_forecast, label='预测值 (ARIMA-Bootstrap)', color='red')
plt.fill_between(np.arange(len(train), len(time_series)), conf_interval_lower, conf_interval_upper, color='gray', alpha=0.3, label='95%置信区间')
plt.xlabel('时间')
plt.ylabel('值')
plt.title('改进的 ARIMA-Bootstrap 时间序列预测')
plt.legend()
plt.show()

# 打印模型AIC和残差
print(f"最佳ARIMA模型的AIC值: {arima_model.aic}")
