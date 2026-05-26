"""
案例:
    使用 SHAP 演示模型特征重要性.

适用场景:
    训练好模型后, 想解释:
        1. 全局来看哪些特征重要.
        2. 单个样本为什么会被模型这样预测.

核心原理:
    SHAP会把一次预测结果拆成每个特征的贡献.
    SHAP值 > 0: 该特征把预测往更大的方向推.
    SHAP值 < 0: 该特征把预测往更小的方向推.
    绝对值越大: 影响越大.

"""


import shap
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
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

print(f'验证集准确率: {model.score(x_valid, y_valid):.4f}')

# 4. 创建SHAP解释器.
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(x_valid)

# 5. 多分类任务会为每个类别生成一组SHAP值.
# 这里以类别0为例, 查看全局平均绝对SHAP值.
class_index = 0
if isinstance(shap_values, list):
    # 旧版本SHAP常见格式: list[class] -> (样本数, 特征数)
    class_shap_values = shap_values[class_index]
else:
    # 新版本SHAP可能返回: (样本数, 特征数, 类别数)
    class_shap_values = shap_values[:, :, class_index]

importance_df = pd.DataFrame({
    'feature': x.columns,
    'mean_abs_shap': abs(class_shap_values).mean(axis=0)
}).sort_values(by='mean_abs_shap', ascending=False)

print(f'类别{class_index}的全局SHAP重要性:')
print(importance_df)

# 6. 查看单个样本的解释.
sample_index = 0
sample_explanation = pd.DataFrame({
    'feature': x.columns,
    'value': x_valid.iloc[sample_index].values,
    'shap_value': class_shap_values[sample_index]
}).sort_values(by='shap_value', key=abs, ascending=False)

print(f'验证集中第{sample_index}个样本对类别{class_index}预测的SHAP解释:')
print(sample_explanation)

# 复习理解:
# 全局重要性: mean_abs_shap越大, 说明这个特征整体越影响模型预测.
# 单样本解释: shap_value为正表示推高该类别预测, 为负表示拉低该类别预测.
