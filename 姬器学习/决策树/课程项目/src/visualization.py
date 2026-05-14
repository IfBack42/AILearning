# -*- coding: utf-8 -*-
"""SVG 可视化：模型对比、混淆矩阵、ROC、特征重要性和决策树结构。"""

from html import escape
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

from config import OUTPUT_DIR


def save_svg(path: Path, width: int, height: int, body: str) -> None:
    """保存 SVG 图片，避免额外依赖 Matplotlib。"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
text {{ font-family: "Microsoft YaHei", SimHei, Arial, sans-serif; fill: #111827; }}
.title {{ font-size: 22px; font-weight: 700; }}
.label {{ font-size: 14px; }}
.small {{ font-size: 12px; }}
</style>
{body}
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def plot_model_comparison(
    baseline_metrics: dict[str, float | np.ndarray],
    tuned_metrics: dict[str, float | np.ndarray],
) -> None:
    """绘制基线模型与调参模型对比图。"""
    items = [
        ("Accuracy", "accuracy"),
        ("Balanced Acc.", "balanced_accuracy"),
        ("F1", "f1"),
        ("AUC", "auc"),
        ("Malignant Recall", "malignant_recall"),
    ]
    parts = [
        '<text x="420" y="36" text-anchor="middle" class="title">基线模型 vs 调参模型</text>',
        '<rect x="540" y="50" width="18" height="18" fill="#94a3b8"/><text x="566" y="64" class="small">未调参决策树</text>',
        '<rect x="540" y="76" width="18" height="18" fill="#2563eb"/><text x="566" y="90" class="small">网格搜索后模型</text>',
    ]
    for index, (label, key) in enumerate(items):
        y = 78 + index * 58
        baseline_value = float(baseline_metrics[key])
        tuned_value = float(tuned_metrics[key])
        baseline_width = 430 * baseline_value
        tuned_width = 430 * tuned_value
        parts.append(f'<text x="170" y="{y + 26}" text-anchor="end" class="label">{escape(label)}</text>')
        parts.append(f'<rect x="210" y="{y}" width="{baseline_width:.1f}" height="18" fill="#94a3b8"/>')
        parts.append(f'<rect x="210" y="{y + 24}" width="{tuned_width:.1f}" height="18" fill="#2563eb"/>')
        parts.append(f'<text x="{218 + baseline_width:.1f}" y="{y + 14}" class="small">{baseline_value:.3f}</text>')
        parts.append(f'<text x="{218 + tuned_width:.1f}" y="{y + 38}" class="small">{tuned_value:.3f}</text>')

    path = OUTPUT_DIR / "Test2_model_comparison.svg"
    save_svg(path, 850, 500, "\n".join(parts))
    print("模型对比图已保存：", path)


def plot_confusion_matrix(cm: np.ndarray, target_names: np.ndarray) -> None:
    """绘制混淆矩阵。"""
    cell, left, top = 120, 130, 90
    max_value = max(int(cm.max()), 1)
    parts = [
        '<text x="230" y="40" text-anchor="middle" class="title">决策树混淆矩阵</text>',
        '<text x="250" y="380" text-anchor="middle" class="label">预测类别</text>',
        '<text x="26" y="215" transform="rotate(-90 26 215)" text-anchor="middle" class="label">真实类别</text>',
    ]

    for i, name in enumerate(target_names):
        parts.append(f'<text x="{left - 20}" y="{top + i * cell + 65}" text-anchor="end" class="label">{escape(str(name))}</text>')
        parts.append(f'<text x="{left + i * cell + 60}" y="{top - 18}" text-anchor="middle" class="label">{escape(str(name))}</text>')

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            value = int(cm[i, j])
            alpha = 0.18 + 0.72 * value / max_value
            x = left + j * cell
            y = top + i * cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="#3b82f6" fill-opacity="{alpha:.3f}" stroke="#ffffff"/>')
            parts.append(f'<text x="{x + cell / 2}" y="{y + cell / 2 + 6}" text-anchor="middle" font-size="28" font-weight="700">{value}</text>')

    path = OUTPUT_DIR / "Test2_confusion_matrix.svg"
    save_svg(path, 500, 420, "\n".join(parts))
    print("混淆矩阵已保存：", path)


def plot_roc_curve(roc_points: np.ndarray, auc_value: float) -> None:
    """绘制 ROC 曲线。"""
    left, top, width, height = 80, 70, 380, 300
    points = []
    for fpr, tpr in roc_points:
        x = left + fpr * width
        y = top + (1 - tpr) * height
        points.append(f"{x:.1f},{y:.1f}")

    parts = [
        '<text x="270" y="36" text-anchor="middle" class="title">决策树 ROC 曲线</text>',
        f'<rect x="{left}" y="{top}" width="{width}" height="{height}" fill="white" stroke="#9ca3af"/>',
        f'<line x1="{left}" y1="{top + height}" x2="{left + width}" y2="{top}" stroke="#9ca3af" stroke-dasharray="6 6"/>',
        f'<polyline points="{" ".join(points)}" fill="none" stroke="#ef4444" stroke-width="3"/>',
        f'<text x="{left + width - 8}" y="{top + height + 34}" text-anchor="end" class="label">假阳性率 FPR</text>',
        f'<text x="{left - 48}" y="{top + 10}" transform="rotate(-90 {left - 48} {top + 10})" text-anchor="end" class="label">真正率 TPR</text>',
        f'<text x="{left + width - 8}" y="{top + height - 16}" text-anchor="end" class="label">AUC = {auc_value:.4f}</text>',
    ]
    path = OUTPUT_DIR / "Test2_roc_curve.svg"
    save_svg(path, 540, 440, "\n".join(parts))
    print("ROC 曲线已保存：", path)


def plot_feature_importance(model: DecisionTreeClassifier, feature_names: list[str]) -> None:
    """绘制 Top 10 特征重要性。"""
    importance = pd.Series(model.feature_importances_, index=feature_names)
    top10 = importance.sort_values(ascending=False).head(10)
    max_value = max(float(top10.max()), 1e-9)
    parts = ['<text x="430" y="36" text-anchor="middle" class="title">决策树 Top 10 特征重要性</text>']

    for index, (name, value) in enumerate(top10.sort_values().items()):
        y = 70 + index * 42
        bar_width = 430 * float(value) / max_value
        parts.append(f'<text x="250" y="{y + 18}" text-anchor="end" class="small">{escape(name)}</text>')
        parts.append(f'<rect x="270" y="{y}" width="{bar_width:.1f}" height="24" fill="#10b981"/>')
        parts.append(f'<text x="{280 + bar_width:.1f}" y="{y + 18}" class="small">{value:.4f}</text>')

    path = OUTPUT_DIR / "Test2_feature_importance.svg"
    save_svg(path, 860, 540, "\n".join(parts))
    print("特征重要性图已保存：", path)


def plot_decision_tree_structure(
    model: DecisionTreeClassifier,
    feature_names: list[str],
    target_names: np.ndarray,
) -> None:
    """绘制前三层决策树结构，并导出完整文本规则。"""
    tree = model.tree_
    max_depth = 3
    nodes: list[dict] = []
    leaf_order = 0

    def walk(node_id: int, depth: int) -> float:
        nonlocal leaf_order
        left = tree.children_left[node_id]
        right = tree.children_right[node_id]
        if depth == max_depth or left == right:
            x_pos = leaf_order
            leaf_order += 1
        else:
            left_x = walk(left, depth + 1)
            right_x = walk(right, depth + 1)
            x_pos = (left_x + right_x) / 2

        values = tree.value[node_id][0]
        class_index = int(np.argmax(values))
        rule = "叶节点"
        if left != right and depth < max_depth:
            rule = f"{feature_names[tree.feature[node_id]]} <= {tree.threshold[node_id]:.2f}"

        nodes.append(
            {
                "id": node_id,
                "depth": depth,
                "x": x_pos,
                "left": left if depth < max_depth else -1,
                "right": right if depth < max_depth else -1,
                "rule": rule,
                "samples": int(tree.n_node_samples[node_id]),
                "value": [int(v) for v in values],
                "cls": str(target_names[class_index]),
            }
        )
        return x_pos

    walk(0, 0)
    by_id = {node["id"]: node for node in nodes}
    x_gap, y_gap = 210, 145
    margin_x, margin_y = 90, 70
    width = max(900, int((leaf_order - 1) * x_gap + margin_x * 2 + 180))
    height = margin_y * 2 + max_depth * y_gap + 120
    parts = ['<text x="50%" y="34" text-anchor="middle" class="title">决策树结构图（前 3 层）</text>']

    for node in nodes:
        for child_key, label, label_y_offset in [("left", "是", -8), ("right", "否", 18)]:
            child_id = node[child_key]
            if child_id in by_id:
                child = by_id[child_id]
                x1 = margin_x + node["x"] * x_gap + 90
                y1 = margin_y + node["depth"] * y_gap + 80
                x2 = margin_x + child["x"] * x_gap + 90
                y2 = margin_y + child["depth"] * y_gap
                parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#6b7280"/>')
                parts.append(f'<text x="{(x1 + x2) / 2:.1f}" y="{(y1 + y2) / 2 + label_y_offset:.1f}" text-anchor="middle" class="small">{label}</text>')

    for node in nodes:
        x = margin_x + node["x"] * x_gap
        y = margin_y + node["depth"] * y_gap
        fill = "#dbeafe" if node["rule"] != "叶节点" else "#dcfce7"
        lines = [
            escape(node["rule"][:34]),
            f"samples = {node['samples']}",
            f"value = {node['value']}",
            f"class = {escape(node['cls'])}",
        ]
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="180" height="82" rx="8" fill="{fill}" stroke="#2563eb"/>')
        for idx, line in enumerate(lines):
            weight = ' font-weight="700"' if idx == 0 else ""
            parts.append(f'<text x="{x + 90:.1f}" y="{y + 18 + idx * 18:.1f}" text-anchor="middle" class="small"{weight}>{line}</text>')

    path = OUTPUT_DIR / "Test2_decision_tree.svg"
    save_svg(path, width, height, "\n".join(parts))
    tree_text_path = OUTPUT_DIR / "Test2_decision_tree_rules.txt"
    tree_text_path.write_text(export_text(model, feature_names=feature_names), encoding="utf-8")
    print("决策树结构图已保存：", path)
    print("决策树文本规则已保存：", tree_text_path)

