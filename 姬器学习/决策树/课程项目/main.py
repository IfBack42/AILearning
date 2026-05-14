# -*- coding: utf-8 -*-
"""
实验2：决策树分类实验

主文件只负责串联流程：
1. 加载并预处理数据
2. 划分训练集和测试集
3. 训练基线模型和调参模型
4. 评估模型
5. 输出可视化和汇报摘要
"""

from src.data_processing import load_dataset, preprocess_data, split_dataset
from src.model_training import (
    collect_metrics,
    evaluate_model,
    train_baseline_tree,
    train_decision_tree,
)
from src.report import write_report
from src.visualization import (
    plot_confusion_matrix,
    plot_decision_tree_structure,
    plot_feature_importance,
    plot_model_comparison,
    plot_roc_curve,
)


def main() -> None:
    x, y, feature_names, target_names = load_dataset()
    print("========== 数据集信息 ==========")
    print("数据集名称：Breast Cancer Wisconsin")
    print("样本数量：", x.shape[0])
    print("特征数量：", x.shape[1])
    print("类别名称：", target_names)

    x_processed = preprocess_data(x)
    x_train, x_test, y_train, y_test = split_dataset(x_processed, y)
    print("\n训练集样本数：", x_train.shape[0])
    print("测试集样本数：", x_test.shape[0])

    baseline_model = train_baseline_tree(x_train, y_train)
    baseline_metrics = collect_metrics(baseline_model, x_test, y_test)

    model = train_decision_tree(x_train, y_train)
    metrics = evaluate_model(model, x_test, y_test, target_names)

    plot_model_comparison(baseline_metrics, metrics)
    plot_confusion_matrix(metrics["cm"], target_names)
    plot_roc_curve(metrics["roc_points"], float(metrics["auc"]))
    plot_feature_importance(model, feature_names)
    plot_decision_tree_structure(model, feature_names, target_names)
    write_report(model, baseline_metrics, metrics, feature_names)

    print("\n实验完成：已生成模型评价结果和可视化图片。")


if __name__ == "__main__":
    main()

