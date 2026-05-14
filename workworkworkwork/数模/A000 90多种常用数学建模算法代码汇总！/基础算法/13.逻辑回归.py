import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. 生成模拟客户行为数据集
np.random.seed(42)
n_samples = 500

# 浏览时间（分钟）随机生成，假设范围在 1 到 50 分钟之间
browsing_time = np.random.randint(1, 50, size=n_samples)

# 浏览产品数量随机生成，假设范围在 1 到 10 之间
num_products_viewed = np.random.randint(1, 10, size=n_samples)

# 购物车中的商品数量随机生成，假设范围在 0 到 5 之间
num_items_in_cart = np.random.randint(0, 5, size=n_samples)

# 生成目标值：假设某些条件下（如长时间浏览和购物车中有多个商品）更可能购买
# 使用一个简单的逻辑函数生成是否购买的数据（购买为1，不购买为0）
# 如果客户浏览时间超过20分钟，浏览产品数超过5，并且购物车中商品数大于2，则购买概率更大
purchased = (browsing_time > 20) & (num_products_viewed > 5) & (num_items_in_cart > 2)
purchased = purchased.astype(int)  # 转换为 0 或 1

# 组合成 DataFrame
df = pd.DataFrame({
    'Browsing Time': browsing_time,
    'Number of Products Viewed': num_products_viewed,
    'Number of Items in Cart': num_items_in_cart,
    'Purchased': purchased
})

# 2. 准备特征和目标值
X = df[['Browsing Time', 'Number of Products Viewed', 'Number of Items in Cart']]  # 特征
y = df['Purchased']  # 目标值

# 将数据集划分为训练集和测试集，80% 用于训练，20% 用于测试
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 使用逻辑回归模型进行训练
log_reg = LogisticRegression(random_state=42)
log_reg.fit(X_train, y_train)

# 4. 对测试集进行预测
y_pred = log_reg.predict(X_test)

# 5. 评估模型性能
accuracy = accuracy_score(y_test, y_pred)
print(f'模型准确率: {accuracy:.2f}')

# 输出混淆矩阵和分类报告
print("混淆矩阵:")
print(confusion_matrix(y_test, y_pred))

print("\n分类报告:")
print(classification_report(y_test, y_pred))

# 6. 可视化预测结果与实际结果的对比
plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_test)), y_test, color='blue', label='实际结果')
plt.scatter(range(len(y_test)), y_pred, color='red', label='预测结果', marker='x')
plt.title('实际购买结果 vs 预测购买结果')
plt.xlabel('测试样本索引')
plt.ylabel('是否购买 (0=不购买, 1=购买)')
plt.legend()
plt.grid(True)
plt.show()
