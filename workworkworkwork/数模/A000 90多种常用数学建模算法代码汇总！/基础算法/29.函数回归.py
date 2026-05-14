import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
# 生成随机数据
np.random.seed(0)
X = 2 - 3 * np.random.normal(0, 1, 20)  # 生成20个输入特征
Y = X - 2 * (X ** 2) + 0.5 * (X ** 3) + np.random.normal(-3, 3, 20)  # 非线性目标值

# 绘制生成的数据
plt.scatter(X, Y, color='b')
plt.title("广告投入与销售额关系图")
plt.xlabel("广告投入")
plt.ylabel("销售额")
plt.show()


# 转换特征为多项式特征，设定多项式的阶数为3
poly_features = PolynomialFeatures(degree=3)
X_poly = poly_features.fit_transform(X.reshape(-1, 1))

# 线性回归拟合多项式特征
model = LinearRegression()
model.fit(X_poly, Y)

# 预测
Y_pred = model.predict(X_poly)

# 计算误差
mse = mean_squared_error(Y, Y_pred)
r2 = r2_score(Y, Y_pred)

# 输出结果
print(f"均方误差: {mse}")
print(f"R2得分: {r2}")

# 绘制拟合曲线
plt.scatter(X, Y, color='b')
plt.plot(np.sort(X), Y_pred[np.argsort(X)], color='r')
plt.title("多项式回归拟合曲线")
plt.xlabel("广告投入")
plt.ylabel("销售额")
plt.show()
