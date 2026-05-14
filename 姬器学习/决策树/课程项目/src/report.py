# -*- coding: utf-8 -*-
"""生成课程汇报 Markdown 摘要。"""

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from config import OUTPUT_DIR


def write_report(
    model: DecisionTreeClassifier,
    baseline_metrics: dict[str, float | np.ndarray],
    tuned_metrics: dict[str, float | np.ndarray],
    feature_names: list[str],
) -> None:
    """输出一份可直接用于汇报的 Markdown 摘要。"""
    importance = pd.Series(model.feature_importances_, index=feature_names)
    top_features = importance.sort_values(ascending=False).head(5)
    cm = tuned_metrics["cm"]
    assert isinstance(cm, np.ndarray)

    lines = [
        "# 决策树乳腺癌分类项目汇报摘要",
        "",
        "## 项目在做什么",
        "使用 Scikit-learn 内置 Breast Cancer Wisconsin 数据集，根据 30 个细胞核形态特征判断肿瘤样本是 malignant（恶性）还是 benign（良性）。",
        "",
        "## 本次优化亮点",
        "- 决策树不再做标准化，保留原始特征单位，规则阈值更容易解释。",
        "- 增加未调参基线模型与风险导向调参模型对比，说明调参收益。",
        "- 调参时加入 class_weight，并用恶性样本召回率作为交叉验证目标。",
        "",
        "## 调参后测试集表现",
        f"- Accuracy：{float(tuned_metrics['accuracy']):.4f}",
        f"- Balanced Accuracy：{float(tuned_metrics['balanced_accuracy']):.4f}",
        f"- F1：{float(tuned_metrics['f1']):.4f}",
        f"- AUC：{float(tuned_metrics['auc']):.4f}",
        f"- 恶性样本召回率：{float(tuned_metrics['malignant_recall']):.4f}",
        "",
        "## 和未调参模型对比",
        f"- 未调参 Balanced Accuracy：{float(baseline_metrics['balanced_accuracy']):.4f}",
        f"- 调参后 Balanced Accuracy：{float(tuned_metrics['balanced_accuracy']):.4f}",
        f"- 未调参 F1：{float(baseline_metrics['f1']):.4f}",
        f"- 调参后 F1：{float(tuned_metrics['f1']):.4f}",
        "",
        "## 混淆矩阵",
        f"- 实际恶性预测恶性：{int(cm[0, 0])}",
        f"- 实际恶性预测良性：{int(cm[0, 1])}",
        f"- 实际良性预测恶性：{int(cm[1, 0])}",
        f"- 实际良性预测良性：{int(cm[1, 1])}",
        "",
        "## Top 5 关键特征",
    ]
    lines.extend([f"- {name}：{value:.4f}" for name, value in top_features.items()])

    path = OUTPUT_DIR / "Test2_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print("汇报摘要已保存：", path)

