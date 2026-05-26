"""
案例:
    使用 Permutation Importance 演示模型特征重要性.

适用场景:
    已经训练好一个模型, 想知道某个特征被打乱后, 模型效果会下降多少.
    下降越多, 说明该特征对模型越重要.

核心原理:
    1. 先在验证集上计算模型得分.
    2. 随机打乱某一列特征.
    3. 再计算模型得分.
    4. 如果得分下降明显, 说明模型很依赖这个特征.

注意:
    Permutation Importance 应该在验证集或测试集上看, 不建议只在训练集上看.
"""

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split


# 1. 读取鸢尾花数据.
iris = load_iris()
x = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target

# 2. 划分训练集和验证集.
x_train, x_valid, y_train, y_valid = train_test_split(
    x,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# 3. 训练一个随机森林分类模型.
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(x_train, y_train)

# 4. 查看原始验证集准确率.
score = model.score(x_valid, y_valid)
print(f'原始验证集准确率: {score:.4f}')

# 5. 计算Permutation Importance.
result = permutation_importance(
    model,
    x_valid,
    y_valid,
    n_repeats=20,
    random_state=42
)

# 6. 整理结果.
importance_df = pd.DataFrame({
    'feature': x.columns,
    'importance_mean': result.importances_mean,
    'importance_std': result.importances_std
}).sort_values(by='importance_mean', ascending=False)

print('Permutation Importance结果:')
print(importance_df)

# 复习理解:
# importance_mean 越大, 表示打乱该特征后模型下降越明显, 该特征越重要.
# 如果两个特征高度相关, 打乱其中一个时另一个可能还能补上, 重要性可能被低估.
