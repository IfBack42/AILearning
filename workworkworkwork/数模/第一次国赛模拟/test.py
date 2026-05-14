import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 模拟时间数据（0到59分钟）
time = np.linspace(0, 59, 60)

# 模拟车流量数据，这里你可以替换成实际的数据
# 例如，随机生成一些数据（实际使用时，应读取附件表中的数据）
traffic_data = [32.5, 34.1, 35.7, 37.3, 38.9, 40.5, 53.1, 54.7, 56.3, 57.9,
         59.5, 61.1, 62.7, 64.3, 51.9, 53.5, 55.1, 56.7, 71.3, 71.9,
         72.5, 73.1, 73.7, 74.3, 74.9, 75.5, 64.5, 64.5, 64.5, 64.5,
         64.5, 64.5, 64.5, 64.5, 75.5, 75.5, 75.5, 75.5, 75.5, 75.9,
         76.3, 76.7, 63.1, 63.5, 63.9, 64.3, 78.7, 79.1, 79.5, 79.9,
         80.3, 80.7, 81.1, 81.5, 70.9, 71.3, 71.7, 72.1, 72.5, 72.9]

# 1. 去除线性趋势
def linear_trend(x, a, b):
    return a * x + b

# 使用最小二乘法拟合线性趋势
popt, _ = curve_fit(linear_trend, time, traffic_data)
trend = linear_trend(time, *popt)

# 去趋势化数据
detrended_data = traffic_data - trend

# 2. 快速傅里叶变换（FFT）分析周期性特征
fft_data = np.fft.fft(detrended_data)
frequencies = np.fft.fftfreq(len(detrended_data), d=2)  # 采样间隔为2分钟

# 取前半部分频率（正频率）
positive_freq = frequencies[:len(frequencies)//2]
positive_fft = np.abs(fft_data[:len(fft_data)//2])

# 绘制频谱图
plt.figure(figsize=(10, 6))
plt.plot(positive_freq, positive_fft)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('FFT of Detrended Traffic Data')
plt.grid(True)
plt.show()

# 通过FFT分析得到的频率估计值
estimated_frequency = positive_freq[np.argmax(positive_fft)]
print("Estimated frequency from FFT:", estimated_frequency)

# 3. 定义周期性模型（傅里叶级数模型）
def periodic_model(t, A, f, phi, offset):
    return A * np.cos(2 * np.pi * f * t + phi) + offset

# 设置初始猜测值
p0 = [np.max(detrended_data) - np.min(detrended_data), estimated_frequency, 0, np.mean(detrended_data)]

# 使用最小二乘法拟合周期性数据
try:
    popt, pcov = curve_fit(periodic_model, time, detrended_data, p0=p0, maxfev=5000)
except RuntimeError as e:
    print("Error:", e)
    print("Initial Parameters:", p0)

# 输出拟合参数
print("Fitted parameters:", popt)

# 绘制拟合结果
fitted_data = periodic_model(time, *popt)
plt.figure(figsize=(10, 6))
plt.plot(time, detrended_data, label='Detrended Data', color='blue')
plt.plot(time, fitted_data, label='Fitted Model', linestyle='--', color='red')
plt.legend()
plt.xlabel('Time (minutes)')
plt.ylabel('Traffic Flow')
plt.title('Traffic Flow and Fitted Model')
plt.grid(True)
plt.show()

# 4. 推测各支路车流量
# 假设你有主路流量数据并能推测各支路流量，我们可以根据拟合结果进行推测。
# 如果知道各支路与主路流量的比例关系，可以在此进行推测
# 例如，如果支路1的车流量占主路车流量的20%，可以这样推测：
# branch1_traffic = 0.2 * fitted_data
# 根据具体情况进行修改

