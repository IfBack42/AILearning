import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import matplotlib.pyplot as plt

# 加载数据
file_path = 'D:\\py\\LearnPython\\data.xlsx'
data = pd.read_excel(file_path)

# 分离输入和输出
X = data.iloc[:, :-1].values  # 输入特征
y = data.iloc[:, -1].values  # 输出目标

# 数据标准化
scaler = StandardScaler()  # 创建StandardScaler对象，用于将输入数据标准化
X_scaled = scaler.fit_transform(X)  # 对输入数据进行标准化

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# 定义LPO算法
def LPO(nPop, MaxIt, VarMin, VarMax, nVar, fobj):
    VarSize = (nVar,)

    class Plant:
        def __init__(self):
            self.Position = None
            self.Cost = None

    pop = [Plant() for _ in range(nPop)]
    BestSol = Plant()
    BestSol.Cost = np.inf

    Delta = np.random.rand(nPop) * 2 * np.pi
    sigma1 = np.random.rand(nPop, nVar)

    BestCost1 = []

    for i in range(nPop):
        pop[i].Position = np.random.uniform(VarMin, VarMax, VarSize)
        pop[i].Cost = fobj(pop[i].Position)
        if pop[i].Cost <= BestSol.Cost:
            BestSol.Position = pop[i].Position.copy()
            BestSol.Cost = pop[i].Cost
        BestCost1.append(BestSol.Cost)

    it = nPop
    Pos1 = np.zeros(nVar)
    while it <= MaxIt:
        Costs = np.array([p.Cost for p in pop])
        BestCost = np.min(Costs)
        WorstCost = np.max(Costs)

        for i in range(nPop):
            R = pop[i].Cost
            C = (R / 2) * np.sin(Delta[i])

            for jj in range(1, 6):
                newsol = Plant()
                newsol2 = Plant()

                if jj == 1:
                    newsol.Position = pop[i].Position + (((R ** 2 + (1 / (2 * np.pi * nVar * R * C) ** 2)) ** -0.5) *
                                                         np.sin(2 * np.pi * nVar * it) *
                                                         np.sin((2 * np.pi * nVar * it) + Delta[i])) * pop[i].Position
                else:
                    newsol.Position = pop[i].Position + (((R ** 2 + (1 / (2 * np.pi * nVar * R * C) ** 2)) ** -0.5) *
                                                         np.sin(2 * np.pi * nVar * it) *
                                                         np.sin((2 * np.pi * nVar * it) + Delta[i])) * Pos1

                A1 = np.random.permutation(nPop)
                A1 = A1[A1 != i]
                a1, a2, a3 = A1[:3]

                aa1 = (pop[a2].Cost - pop[a3].Cost) / abs(pop[a3].Cost - pop[a2].Cost)
                if (pop[a2].Cost - pop[a3].Cost) == 0:
                    aa1 = 1

                aa2 = (pop[a1].Cost - pop[i].Cost) / abs(pop[a1].Cost - pop[i].Cost)
                if (pop[a1].Cost - pop[i].Cost) == 0:
                    aa2 = 1

                newsol.Position = newsol.Position + (aa2 * sigma1[i]) * (newsol.Position - pop[a1].Position) + \
                                  (aa1 * sigma1[i]) * (pop[a3].Position - pop[a2].Position)

                newsol2.Position = pop[a1].Position + (sigma1[i]) * (pop[a3].Position - pop[a2].Position)

                for j in range(nVar):
                    if np.random.rand() > (np.random.rand() / jj):
                        Pos1[j] = newsol2.Position[j]
                    else:
                        Pos1[j] = newsol.Position[j]

                Pos1 = np.maximum(Pos1, VarMin)
                Pos1 = np.minimum(Pos1, VarMax)

                newsol.Position = Pos1
                Delta[i] = np.arctan((1 / (2 * np.pi * nVar * R * C)))

                newsol.Cost = fobj(newsol.Position)

                if newsol.Cost < pop[i].Cost:
                    pop[i] = newsol
                    if pop[i].Cost <= BestSol.Cost:
                        BestSol = pop[i]
                it += 1

                BestCost1.append(BestSol.Cost)
                sigma1[i] = np.random.rand(nVar)

        if it % 180 == 0:
            print(f'Iteration {it}: Best Cost = {BestSol.Cost}')

    return BestSol, BestCost1


# 定义优化目标函数
def objective_function(params):
    n_estimators = int(params[0])
    learning_rate = max(0.01, min(0.3, params[1]))  # 确保 learning_rate 在 [0.01, 0.3] 范围内
    max_depth = int(params[2])
    subsample = max(0.01, min(1, params[3]))  # 确保 subsample 在 [0, 1] 范围内
    colsample_bytree = max(0.01, min(1, params[4]))  # 确保 colsample_bytree 在 [0, 1] 范围内

    model = xgb.XGBRegressor(n_estimators=n_estimators,
                             learning_rate=learning_rate,
                             max_depth=max_depth,
                             subsample=subsample,
                             colsample_bytree=colsample_bytree,
                             objective='reg:squarederror',
                             random_state=42)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return mse


# 定义参数范围
VarMin = [50, 0.01, 3, 0.01, 0.01]
VarMax = [500, 0.3, 10, 1.0, 1.0]  # 增加范围

# 调用LPO优化
nPop = 100  # 增加种群大小
MaxIt = 1000  # 增加迭代次数
nVar = 5

best_solution, best_cost_history = LPO(nPop=nPop, MaxIt=MaxIt, VarMin=VarMin, VarMax=VarMax, nVar=nVar,
                                       fobj=objective_function)

# 提取最佳参数
best_params = best_solution.Position
n_estimators = int(best_params[0])
learning_rate = max(0.01, min(0.3, best_params[1]))  # 确保 learning_rate 在 [0.01, 0.3] 范围内
max_depth = int(best_params[2])
subsample = max(0.01, min(1, best_params[3]))  # 确保 subsample 在 [0, 1] 范围内
colsample_bytree = max(0.01, min(1, best_params[4]))  # 确保 colsample_bytree 在 [0, 1] 范围内

# 使用最佳参数训练模型
optimized_model = xgb.XGBRegressor(n_estimators=n_estimators,
                                   learning_rate=learning_rate,
                                   max_depth=max_depth,
                                   subsample=subsample,
                                   colsample_bytree=colsample_bytree,
                                   objective='reg:squarederror',
                                   random_state=42)

optimized_model.fit(X_train, y_train)
y_pred_optimized = optimized_model.predict(X_test)

# 评估优化后的模型性能
mse_optimized = mean_squared_error(y_test, y_pred_optimized)
r2_optimized = r2_score(y_test, y_pred_optimized)
rmse_optimized = np.sqrt(mse_optimized)
mae_optimized = mean_absolute_error(y_test, y_pred_optimized)
mape_optimized = np.mean(np.abs((y_test - y_pred_optimized) / (y_test + 1e-10))) * 100  # 添加小常数避免除零

# 输出最佳模型性能和配置
print("Optimized model performance:")
print(f"MSE: {mse_optimized:.4f}")
print(f"R2: {r2_optimized:.4f}")
print(f"RMSE: {rmse_optimized:.4f}")
print(f"MAE: {mae_optimized:.4f}")
print(f"MAPE: {mape_optimized:.4f}%")
print("Optimized model configuration:", best_params)

# 未优化的模型
default_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
default_model.fit(X_train, y_train)
y_pred_default = default_model.predict(X_test)

# 评估未优化的模型性能
mse_default = mean_squared_error(y_test, y_pred_default)
r2_default = r2_score(y_test, y_pred_default)
rmse_default = np.sqrt(mse_default)
mae_default = mean_absolute_error(y_test, y_pred_default)
mape_default = np.mean(np.abs((y_test - y_pred_default) / (y_test + 1e-10))) * 100  # 添加小常数避免除零

print("Default model performance:")
print(f"MSE: {mse_default:.4f}")
print(f"R2: {r2_default:.4f}")
print(f"RMSE: {rmse_default:.4f}")
print(f"MAE: {mae_default:.4f}")
print(f"MAPE: {mape_default:.4f}%")

# 可视化预测结果，展示测试集的真实值与最佳模型的预测值对比
plt.figure(figsize=(10, 6))
plt.plot(range(len(y_test)), y_test, color='blue', label='Actual Values')
plt.plot(range(len(y_pred_optimized)), y_pred_optimized, color='red', label='Optimized Predictions')
plt.plot(range(len(y_pred_default)), y_pred_default, color='green', label='Default Predictions')
plt.title('Optimized vs Default XGBoost Regression Predictions on Test Set')
plt.xlabel('Index')
plt.ylabel('Target Value')
plt.legend()
plt.grid(True)
plt.show()

