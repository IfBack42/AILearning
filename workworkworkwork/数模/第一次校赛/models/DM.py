import numpy as np
import pandas as pd
from scipy.stats import norm


def diebold_mariano_test(e1, e2, h=1):
    d = e1 - e2
    T = len(d)
    mean_d = np.mean(d)

    gamma_0 = np.var(d)
    gamma_h = np.cov(d[:-h], d[h:])[0, 1]

    dm_stat = mean_d / np.sqrt((gamma_0 + 2 * gamma_h) / T)
    p_value = 2 * (1 - norm.cdf(abs(dm_stat)))

    return dm_stat, p_value


# 读取CSV文件
data = pd.read_csv('../data.csv')

# 提取模型预测值
lstm_forecasts = data['LSTM'].str.extract(r'(\d+\.\d+)')[0].astype(float).values
arima_forecasts = data['ARIMA'].str.extract(r'(\d+\.\d+)')[0].astype(float).values
rf_forecasts = data['随机森林'].str.extract(r'(\d+\.\d+)')[0].astype(float).values

# 由于缺少实际观测值，这里我们只能计算模型预测值之间的差异
e1 = lstm_forecasts
e2 = arima_forecasts
e3 = rf_forecasts

# 对三个模型的两两组合进行DM检验
dm12_stat, dm12_p = diebold_mariano_test(e1, e2)
dm13_stat, dm13_p = diebold_mariano_test(e1, e3)
dm23_stat, dm23_p = diebold_mariano_test(e2, e3)

# 输出结果
print("DM检验结果：")
print(f"LSTM vs ARIMA: DM Statistic = {dm12_stat}, p-value = {dm12_p}")
print(f"LSTM vs 随机森林: DM Statistic = {dm13_stat}, p-value = {dm13_p}")
print(f"ARIMA vs 随机森林: DM Statistic = {dm23_stat}, p-value = {dm23_p}")