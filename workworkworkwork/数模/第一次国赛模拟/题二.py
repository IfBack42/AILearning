def extract_period_from_stable_segment(y_data):
    """
    从支路2稳定时间段提取周期信息
    :param y_data: 完整车流量数据
    :return: 估计的周期（时间步长）
    """
    # 提取稳定时间段
    stable_segment = y_data[25:39]  # t=25到38
    t_segment = np.arange(len(stable_segment))

    # 去线性趋势
    slope, intercept, _, _, _ = stats.linregress(t_segment, stable_segment)
    detrended = stable_segment - (intercept + slope * t_segment)

    # FFT分析
    n = len(detrended)
    yf = fft(detrended - np.mean(detrended))
    xf = fftfreq(n, 1)[:n // 2]
    power = np.abs(yf[0:n // 2]) ** 2

    # 找到主要周期
    valid_freq = xf > 0
    dominant_period = 1 / xf[valid_freq][np.argmax(power[valid_freq])]

    # 合理性检查
    if dominant_period < 5 or dominant_period > 30:
        # 使用自相关法作为备选
        autocorr = np.correlate(detrended, detrended, mode='full')
        autocorr = autocorr[len(autocorr) // 2:]
        peaks = np.where(autocorr > 0.5 * np.max(autocorr))[0]
        if len(peaks) > 1:
            dominant_period = peaks[1]
        else:
            dominant_period = 10  # 默认值

    return dominant_period


def full_traffic_model(y_data):
    """
    完整车流量模型
    :param y_data: 主路车流量数据
    :return: 优化后的参数
    """
    # 1. 估计支路4周期
    period_estimate = extract_period_from_stable_segment(y_data)
    print(f"估计的支路4周期: {period_estimate:.2f} 时间步长 ({period_estimate * 2:.2f} 分钟)")

    # 2. 设置模型参数和初始值
    # [这里接之前提供的完整模型代码]
    # ...

    # 在优化中包含周期参数
    # ...

    return optimized_params

# 使用实际数据运行模型
# params = full_traffic_model(y_data)