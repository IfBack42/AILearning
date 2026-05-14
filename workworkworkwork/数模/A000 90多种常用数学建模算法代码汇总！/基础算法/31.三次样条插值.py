# 导入必要的库
import numpy as np  # 用于数值计算
import matplotlib.pyplot as plt  # 用于绘图
from scipy.interpolate import CubicSpline  # 用于三次样条插值

# 1. 生成数据点
# 我们生成一些随机数据点用于插值
x = np.linspace(0, 10, 10)  # 生成x坐标，10个均匀分布的数据点
y = np.sin(x)  # 对应的y值是x的正弦函数

# 2. 创建三次样条插值函数
cs = CubicSpline(x, y)  # 使用生成的x和y创建三次样条插值对象

# 3. 插值与可视化
# 为了更加平滑，我们在原始数据点之间生成更多的点
x_new = np.linspace(0, 10, 100)  # 在0到10之间生成100个新的x值
y_new = cs(x_new)  # 对新x值进行插值，计算对应的y值

# 4. 绘图
plt.figure(figsize=(8, 6))  # 设置图形的大小
plt.plot(x, y, 'o', label='原始数据点', color='red')  # 绘制原始数据点，红色圆圈表示
plt.plot(x_new, y_new, label='三次样条插值', color='blue')  # 绘制插值结果，蓝色线条表示
plt.xlabel('X')  # 设置x轴标签
plt.ylabel('Y')  # 设置y轴标签
plt.title('三次样条插值')  # 设置图形标题
plt.legend()  # 显示图例
plt.grid(True)  # 显示网格线
plt.show()  # 展示图形
