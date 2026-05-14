# 导入必要的库
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 1. 读取数据
data_path = 'D:/py/LearnPython/data0.xlsx'  # 数据路径
data = pd.read_excel(data_path)  # 读取数据
X = data.iloc[:, :-1].values  # 输入特征
Y = data.iloc[:, -1].values  # 输出目标

# 2. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. K-Means聚类
kmeans = KMeans(n_clusters=3, random_state=42)
X_cluster_labels = kmeans.fit_predict(X_scaled)

# 将聚类标签加入到数据集中
clustered_data = pd.DataFrame(X_scaled, columns=[f'feature_{i}' for i in range(X_scaled.shape[1])])
clustered_data['target'] = Y
clustered_data['cluster'] = X_cluster_labels

# 4. 定义XGBoost回归模型的超参数
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [3, 5],
    'learning_rate': [0.01, 0.1]
}

# 5. 对每个类别的样本分别构建XGBoost回归模型并进行超参数优化
results = {}

for cluster in np.unique(X_cluster_labels):
    print(f"\n类别 {cluster}:")

    # 提取该类别的数据
    cluster_data = clustered_data[clustered_data['cluster'] == cluster]
    X_cluster = cluster_data.drop(columns=['target', 'cluster']).values
    Y_cluster = cluster_data['target'].values

    # 将数据划分为训练集和测试集
    X_train, X_test, Y_train, Y_test = train_test_split(X_cluster, Y_cluster, test_size=0.2, random_state=42)

    # 使用GridSearchCV进行超参数搜索
    xgb_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error',
                               n_jobs=-1)
    grid_search.fit(X_train, Y_train)

    # 获取最佳模型
    best_model = grid_search.best_estimator_

    # 在训练集和测试集上进行预测
    Y_pred_train = best_model.predict(X_train)
    Y_pred_test = best_model.predict(X_test)

    # 计算误差
    train_mse = mean_squared_error(Y_train, Y_pred_train)
    test_mse = mean_squared_error(Y_test, Y_pred_test)
    train_r2 = r2_score(Y_train, Y_pred_train)
    test_r2 = r2_score(Y_test, Y_pred_test)

    # 输出结果
    print(f"训练集 MSE: {train_mse:.4f}, R²: {train_r2:.4f}")
    print(f"测试集 MSE: {test_mse:.4f}, R²: {test_r2:.4f}")

    # 保存结果
    results[cluster] = {
        'train_mse': train_mse,
        'test_mse': test_mse,
        'train_r2': train_r2,
        'test_r2': test_r2
    }

# 6. 绘制聚类后的散点图（如果特征数较多，只绘制前两列特征）
plt.figure(figsize=(10, 6))
for cluster in np.unique(X_cluster_labels):
    cluster_data = clustered_data[clustered_data['cluster'] == cluster]
    plt.scatter(cluster_data.iloc[:, 0], cluster_data.iloc[:, 1], label=f'Cluster {cluster}')
plt.title('K-Means聚类结果')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.grid(True)
plt.show()

# 打印所有类别的误差结果
for cluster, result in results.items():
    print(f"类别 {cluster}: 训练集 MSE: {result['train_mse']:.4f}, 测试集 MSE: {result['test_mse']:.4f}, "
          f"训练集 R²: {result['train_r2']:.4f}, 测试集 R²: {result['test_r2']:.4f}")
