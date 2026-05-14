# -*- coding: utf-8 -*-
"""决策树训练、调参、预测和评价。"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    auc,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

from config import RANDOM_STATE


def train_baseline_tree(x_train: pd.DataFrame, y_train: pd.Series) -> DecisionTreeClassifier:
    """训练未调参决策树，作为对照组。"""
    model = DecisionTreeClassifier(random_state=RANDOM_STATE)
    model.fit(x_train, y_train)
    return model


def train_decision_tree(x_train: pd.DataFrame, y_train: pd.Series) -> DecisionTreeClassifier:
    """使用网格搜索训练风险导向的决策树模型。"""
    param_grid = {
        "criterion": ["gini", "entropy"],
        "max_depth": [2, 3, 4, 5, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "class_weight": [None, "balanced", {0: 1.5, 1: 1}, {0: 2, 1: 1}],
    }

    scorer = make_scorer(recall_score, pos_label=0)
    grid_search = GridSearchCV(
        estimator=DecisionTreeClassifier(random_state=RANDOM_STATE),
        param_grid=param_grid,
        cv=5,
        scoring=scorer,
        n_jobs=1,
        return_train_score=True,
    )
    grid_search.fit(x_train, y_train)

    print("\n========== 模型训练 ==========")
    print("最优参数：", grid_search.best_params_)
    print(f"交叉验证最佳恶性召回率：{grid_search.best_score_:.4f}")
    return grid_search.best_estimator_


def collect_metrics(
    model: DecisionTreeClassifier,
    x_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float | np.ndarray]:
    """计算分类指标、混淆矩阵和 ROC 点。"""
    y_pred = model.predict(x_test)
    y_proba = model.predict_proba(x_test)[:, 1]
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    fpr, tpr, _ = roc_curve(y_test, y_proba)

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "auc": auc(fpr, tpr),
        "malignant_recall": cm[0, 0] / max(cm[0].sum(), 1),
        "benign_recall": cm[1, 1] / max(cm[1].sum(), 1),
        "cm": cm,
        "roc_points": np.column_stack((fpr, tpr)),
    }


def evaluate_model(
    model: DecisionTreeClassifier,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    target_names: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """输出预测预览和模型评价指标。"""
    y_pred = model.predict(x_test)
    y_proba = model.predict_proba(x_test)[:, 1]
    metrics = collect_metrics(model, x_test, y_test)

    print("\n========== 预测结果 ==========")
    preview = pd.DataFrame(
        {
            "真实标签": y_test.to_numpy()[:20],
            "预测标签": y_pred[:20],
            "预测为 benign 的概率": np.round(y_proba[:20], 4),
        }
    )
    print(preview.to_string(index=False))

    print("\n========== 模型评价 ==========")
    print(f"准确率 Accuracy：{metrics['accuracy']:.4f}")
    print(f"平衡准确率 Balanced Accuracy：{metrics['balanced_accuracy']:.4f}")
    print(f"精确率 Precision：{metrics['precision']:.4f}")
    print(f"召回率 Recall：{metrics['recall']:.4f}")
    print(f"F1 分数：{metrics['f1']:.4f}")
    print(f"AUC 值：{metrics['auc']:.4f}")
    print(f"恶性样本召回率：{metrics['malignant_recall']:.4f}")
    print("\n分类报告：")
    print(classification_report(y_test, y_pred, target_names=target_names))
    return metrics

