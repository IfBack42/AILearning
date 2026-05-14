# 决策树乳腺癌分类项目汇报摘要

## 项目在做什么
使用 Scikit-learn 内置 Breast Cancer Wisconsin 数据集，根据 30 个细胞核形态特征判断肿瘤样本是 malignant（恶性）还是 benign（良性）。

## 本次优化亮点
- 决策树不再做标准化，保留原始特征单位，规则阈值更容易解释。
- 增加未调参基线模型与风险导向调参模型对比，说明调参收益。
- 调参时加入 class_weight，并用恶性样本召回率作为交叉验证目标。

## 调参后测试集表现
- Accuracy：0.9357
- Balanced Accuracy：0.9266
- F1：0.9493
- AUC：0.9205
- 恶性样本召回率：0.8906

## 和未调参模型对比
- 未调参 Balanced Accuracy：0.9126
- 调参后 Balanced Accuracy：0.9266
- 未调参 F1：0.9346
- 调参后 F1：0.9493

## 混淆矩阵
- 实际恶性预测恶性：57
- 实际恶性预测良性：7
- 实际良性预测恶性：4
- 实际良性预测良性：103

## Top 5 关键特征
- worst perimeter：0.7940
- worst compactness：0.0724
- mean concave points：0.0513
- concavity error：0.0324
- area error：0.0216