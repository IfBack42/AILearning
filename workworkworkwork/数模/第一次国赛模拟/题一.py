import numpy as np
import pandas as pd
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimSun"]
plt.rcParams["axes.unicode_minus"] = False


# 修复1：正确读取数据，自动确定数据点数量
df = pd.read_csv('./data_1.txt', header=None, skiprows=1,
                 names=['时间 t (Time t)', '时刻 (Moment)', '主路3的车流量 (Traffic flow on the Main road 3)'])
F_obs = df['主路3的车流量 (Traffic flow on the Main road 3)'].values
time = df['时刻 (Moment)'].str.strip().values
n = len(F_obs)  # 实际数据点数量
t = np.linspace(0, n - 1, n)  # 根据实际数据长度创建时间点


# 修复2：模型函数保持不变
def model(params, t):
    a1, b1, a2, b2, a3, t0 = params
    f1 = a1 * t + b1
    f2 = np.where(t <= t0, a2 * t + b2, -a3 * (t - t0) + (a2 * t0 + b2))
    return f1 + f2


# 修复3：残差函数简化
def residual(params, t, F_obs):
    return model(params, t) - F_obs


# 参数约束
bounds = ([0, 0, 0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf, np.inf, n-1])

# 全局搜索转折点
best_params = None
best_error = np.inf

for candidate_t0 in np.arange(0, n, 1):
    params_init = [0.5, 5.0, 0.5, 5.0, 0.5, candidate_t0]

    res = least_squares(
        residual,
        params_init,
        args=(t, F_obs),
        bounds=bounds,
        method='trf'
    )

    error = np.sum(res.fun ** 2)
    if error < best_error:
        best_error = error
        best_params = res.x

# 精修优化
res_refined = least_squares(
    residual,
    best_params,
    args=(t, F_obs),
    bounds=bounds,
    method='trf'
)

# 提取结果
a1, b1, a2, b2, a3, t0_opt = res_refined.x
print(f"优化结果: a1={a1:.4f}, b1={b1:.4f}, a2={a2:.4f}, b2={b2:.4f}, a3={a3:.4f}, t0={t0_opt:.2f}")
print(f"转折点时间: {df.iloc[int(round(t0_opt))]['时刻 (Moment)']}")
print(f"最小二乘误差: {np.sum(res_refined.fun ** 2):.4f}")

# 可视化
plt.figure(figsize=(8, 4),dpi=150)
plt.plot(t, model(res_refined.x, t), 'r-', label='拟合曲线')
plt.scatter(t, F_obs, s=10, label='观测数据',color='black')
plt.axvline(x=t0_opt, color='green', linestyle='--', label=f'转折点(t={t0_opt:.2f})')
# plt.title('主路3车流量变化拟合',fontsize=11)
plt.xlabel('时间 t (Time t)',fontsize=13)
plt.ylabel('主路3的车流量 (Traffic flow on the Main road 3)',fontsize=11)
# plt.xticks(time[::10],fontsize=13)
# plt.yticks(F_obs[::5],fontsize=13)
plt.legend()
plt.grid(True)
plt.tight_layout()  # 紧密布局，防止标题被砍头

# plt.savefig('traffic_fit.png')
plt.show()

