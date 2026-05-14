import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

# 1. 加载自定义字体
font_path = r'C:\Users\12595\Desktop\STZHONGS.TTF'  # 你的字体路径
custom_font = font_manager.FontProperties(fname=font_path)

# 2. 生成模拟数据
np.random.seed(42)
n_samples = 100  # 样本数量
n_features = 50  # 高维特征数量

# 随机生成设计矩阵 X 和真实参数 beta
X = np.random.randn(n_samples, n_features)
beta_true = np.random.randn(n_features)

# 添加噪声生成 y
noise = np.random.randn(n_samples) * 0.1
y = X @ beta_true + noise


# 贝叶斯线性回归推断
def bayesian_linear_regression(X, y, sigma2, lambda2):
    # 先验的协方差矩阵
    prior_cov = lambda2 * np.eye(X.shape[1])

    # 似然的协方差矩阵
    likelihood_cov = sigma2 * np.eye(X.shape[0])

    # 后验协方差
    posterior_cov = np.linalg.inv(np.linalg.inv(prior_cov) + (1 / sigma2) * X.T @ X)

    # 后验均值
    posterior_mean = posterior_cov @ X.T @ y / sigma2

    return posterior_mean, posterior_cov


# 参数设置
sigma2 = 0.1  # 噪声方差
lambda2 = 1.0  # 先验方差

# 执行贝叶斯线性回归推断
posterior_mean, posterior_cov = bayesian_linear_regression(X, y, sigma2, lambda2)

# 打印后验均值和前 5 个系数的后验标准差
print("后验均值 (前 5 个系数):", posterior_mean[:5])
print("后验标准差 (前 5 个系数):", np.sqrt(np.diag(posterior_cov))[:5])

# 可视化真实系数与后验均值的比较
plt.figure(figsize=(10, 6))
plt.plot(beta_true, label="真实系数", marker='o', color='blue')
plt.plot(posterior_mean, label="后验均值", marker='x', color='red')
plt.fill_between(np.arange(n_features),
                 posterior_mean - np.sqrt(np.diag(posterior_cov)),
                 posterior_mean + np.sqrt(np.diag(posterior_cov)),
                 color='gray', alpha=0.2, label="后验不确定性")

# 设置字体为自定义字体
plt.xlabel("系数索引", fontproperties=custom_font)
plt.ylabel("系数值", fontproperties=custom_font)
plt.title("贝叶斯线性回归的系数推断", fontproperties=custom_font)
plt.legend(prop=custom_font)
plt.grid(True)
plt.show()
