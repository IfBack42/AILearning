import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import matplotlib.font_manager as font_manager

# 设置字体路径
font_path = r'C:\Users\12595\Desktop\STZHONGS.TTF'

# 加载自定义字体
custom_font = font_manager.FontProperties(fname=font_path)

# 设置全局字体配置
plt.rcParams['font.family'] = custom_font.get_name()
plt.rcParams['font.size'] = 12  # 字体大小设置为12

# 1. 生成 GARCH(1,1) 模型的数据
def generate_garch(T, omega, alpha, beta):
    """
    生成 GARCH(1,1) 模型的模拟数据
    参数:
    - T: 样本长度
    - omega: 常数项
    - alpha: ARCH 项系数
    - beta: GARCH 项系数
    返回:
    - eps: 模拟的收益率
    - sigma2: 条件方差序列
    """
    np.random.seed(42)  # 设置随机种子以复现结果
    eps = np.zeros(T)  # 残差项
    sigma2 = np.zeros(T)  # 条件方差

    # 初始化第一期的条件方差
    sigma2[0] = omega / (1 - alpha - beta)
    eps[0] = np.random.normal(0, np.sqrt(sigma2[0]))  # 正态分布噪声

    # 迭代生成 GARCH(1,1) 模型数据
    for t in range(1, T):
        sigma2[t] = omega + alpha * eps[t-1]**2 + beta * sigma2[t-1]
        eps[t] = np.random.normal(0, np.sqrt(sigma2[t]))

    return eps, sigma2

# 模型参数
T = 1000  # 样本长度
omega = 0.1  # 常数项
alpha = 0.2  # ARCH 项
beta = 0.7   # GARCH 项

# 生成模拟数据
returns, sigma2_true = generate_garch(T, omega, alpha, beta)

# 绘制生成的收益率和真实波动性
plt.figure(figsize=(12, 6))
plt.plot(returns, label="收益率", color='blue')
plt.plot(np.sqrt(sigma2_true), label="真实波动性", linestyle='--', color='orange')
plt.title("GARCH(1,1) 模拟的收益率和真实波动性", fontproperties=custom_font)
plt.xlabel("时间", fontproperties=custom_font)
plt.ylabel("波动性", fontproperties=custom_font)
plt.legend(prop=custom_font)
plt.show()

# 2. GARCH(1,1) 模型的对数似然函数
def garch_loglik(params, data):
    """
    GARCH(1,1) 模型的对数似然函数
    参数:
    - params: GARCH 模型参数 [omega, alpha, beta]
    - data0: 时间序列数据（如收益率）
    返回:
    - 负对数似然值（我们需要最大化对数似然，因此返回负值用于最小化）
    """
    omega, alpha, beta = params
    T = len(data)
    sigma2 = np.zeros(T)  # 存储条件方差

    # 初始化条件方差
    sigma2[0] = np.var(data)  # 以样本方差初始化
    loglik = 0  # 对数似然值初始化

    # 计算对数似然值
    for t in range(1, T):
        sigma2[t] = omega + alpha * data[t-1]**2 + beta * sigma2[t-1]
        loglik += -0.5 * (np.log(2 * np.pi) + np.log(sigma2[t]) + data[t]**2 / sigma2[t])

    return -loglik  # 返回负对数似然值用于最小化

# 初始猜测参数
initial_params = [0.1, 0.1, 0.8]

# 使用 scipy 的 minimize 函数进行参数估计
result = minimize(garch_loglik, initial_params, args=(returns,), method='L-BFGS-B',
                  bounds=[(1e-6, None), (1e-6, 1), (1e-6, 1)])

# 打印估计的参数
omega_hat, alpha_hat, beta_hat = result.x
print(f"估计的参数: omega={omega_hat:.4f}, alpha={alpha_hat:.4f}, beta={beta_hat:.4f}")

# 3. 预测未来波动性
def predict_volatility(returns, omega_hat, alpha_hat, beta_hat, horizon=10):
    """
    使用 GARCH(1,1) 模型参数预测未来的波动性
    参数:
    - returns: 历史收益率数据
    - omega_hat: 估计的 omega 参数
    - alpha_hat: 估计的 alpha 参数
    - beta_hat: 估计的 beta 参数
    - horizon: 预测的时间跨度（如未来 10 天）
    返回:
    - 预测的波动性序列
    """
    T = len(returns)
    sigma2_pred = np.zeros(horizon)
    sigma2_last = omega_hat + alpha_hat * returns[-1]**2 + beta_hat * np.var(returns)

    # 迭代预测未来的波动性
    for t in range(horizon):
        sigma2_pred[t] = omega_hat + alpha_hat * returns[-1]**2 + beta_hat * sigma2_last
        sigma2_last = sigma2_pred[t]

    return sigma2_pred

# 预测未来 10 天的波动性
horizon = 10
sigma2_pred = predict_volatility(returns, omega_hat, alpha_hat, beta_hat, horizon)

# 绘制预测的波动性
plt.figure(figsize=(10, 6))
plt.plot(np.sqrt(sigma2_pred), marker='o', linestyle='-', color='green')
plt.title(f"未来 {horizon} 天的波动性预测", fontproperties=custom_font)
plt.xlabel("天数", fontproperties=custom_font)
plt.ylabel("预测波动率", fontproperties=custom_font)
plt.show()
