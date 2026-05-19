from collections import Counter

from config import BASE_FEATURES, DATA_FILE, K_VALUES, OUTPUT_DIR, SAMPLE_SIZE, TOP_GENRES, TOP_TAGS
from data_loader import load_games
from model import build_matrix, evaluate_knn_for_k_values, fit_scaler, transform
from preprocessing import add_features, deduplicate_games, stratified_sample, top_values, train_test_split
from reporting import write_csv, write_report
from visualization import svg_bar_chart, svg_scatter


def build_feature_names(top_genres, top_tags):
    """组合基础数值特征、热门类型特征和热门标签特征。"""
    genre_features = [f"genre_{name}" for name in top_genres]
    tag_features = [f"tag_{name}" for name in top_tags]
    return BASE_FEATURES + genre_features + tag_features


def train_and_select_k(train_rows, test_rows, feature_names):
    """完成标准化、KNN 训练评估，并从多个 K 值中选择最优结果。"""
    train_x = build_matrix(train_rows, feature_names)
    test_x = build_matrix(test_rows, feature_names)

    means, stds = fit_scaler(train_x)
    train_x = transform(train_x, means, stds)
    test_x = transform(test_x, means, stds)

    train_y = [row["target"] for row in train_rows]
    test_y = [row["target"] for row in test_rows]

    metrics_rows = []
    best = None
    results_by_k = evaluate_knn_for_k_values(train_x, train_y, test_x, test_y, K_VALUES)
    for k, result in results_by_k.items():
        metrics_rows.append({"k": k, "accuracy": result["accuracy"], "macro_f1": result["macro_f1"]})
        if best is None or result["macro_f1"] > best[1]["macro_f1"]:
            best = (k, result)

    return best, metrics_rows


def build_confusion_rows(matrix):
    """把混淆矩阵从字典结构转换成方便写入 CSV 的行数据。"""
    labels = sorted(matrix.keys())
    rows = []

    for actual in labels:
        row = {"actual": actual}
        for pred in labels:
            row[pred] = matrix[actual][pred]
        rows.append(row)

    return labels, rows


def save_tables(featured, metrics_rows, confusion_rows, labels):
    """保存清洗样例、K 值评估结果和混淆矩阵三个 CSV 文件。"""
    preview_columns = [
        "name",
        "release_year",
        "positive_rate",
        "review_count",
        "price",
        "rating_name",
        "target",
        "genres_text",
        "tags_text",
        "developer",
    ]

    write_csv(OUTPUT_DIR / "cleaned_sample.csv", featured[:200], preview_columns)
    write_csv(OUTPUT_DIR / "metrics.csv", metrics_rows, ["k", "accuracy", "macro_f1"])
    write_csv(OUTPUT_DIR / "confusion_matrix.csv", confusion_rows, ["actual"] + labels)


def save_visualizations(clean_rows, featured):
    """生成课程汇报中要用到的几张 SVG 可视化图表。"""
    target_counts = Counter(row["target"] for row in featured)
    svg_bar_chart(
        OUTPUT_DIR / "rating_distribution.svg",
        "Rating Group Distribution",
        [name for name, _ in target_counts.most_common()],
        [count for _, count in target_counts.most_common()],
        color="#2563eb",
    )

    genre_counts = Counter()
    tag_counts = Counter()
    for row in clean_rows:
        genre_counts.update(row["genres"])
        tag_counts.update(row["tags"])

    svg_bar_chart(
        OUTPUT_DIR / "top_genres.svg",
        "Top Genres",
        [name for name, _ in genre_counts.most_common(12)],
        [count for _, count in genre_counts.most_common(12)],
        color="#0f766e",
    )
    svg_bar_chart(
        OUTPUT_DIR / "top_tags.svg",
        "Top Tags",
        [name for name, _ in tag_counts.most_common(12)],
        [count for _, count in tag_counts.most_common(12)],
        color="#7c3aed",
    )

    scatter_rows = sorted(featured, key=lambda row: row["review_count"], reverse=True)[:1500]
    svg_scatter(OUTPUT_DIR / "price_positive_scatter.svg", "Price vs Positive Rate", scatter_rows)


def main():
    """项目主流程：从读取数据到训练模型，再到导出图表和汇报。"""
    OUTPUT_DIR.mkdir(exist_ok=True)

    rows, _, _, _ = load_games(DATA_FILE)
    clean_rows = deduplicate_games(rows)

    top_genres = top_values(clean_rows, "genres", TOP_GENRES)
    top_tags = top_values(clean_rows, "tags", TOP_TAGS)
    featured = add_features(clean_rows, top_genres, top_tags)
    feature_names = build_feature_names(top_genres, top_tags)

    sample = stratified_sample(featured, SAMPLE_SIZE)
    train_rows, test_rows = train_test_split(sample)
    (best_k, best_result), metrics_rows = train_and_select_k(train_rows, test_rows, feature_names)

    labels, confusion_rows = build_confusion_rows(best_result["matrix"])
    save_tables(featured, metrics_rows, confusion_rows, labels)
    save_visualizations(clean_rows, featured)

    summary = {
        "raw_count": len(rows),
        "clean_count": len(clean_rows),
        "sample_size": len(sample),
        "top_genres": TOP_GENRES,
        "top_tags": TOP_TAGS,
        "best_k": best_k,
        "accuracy": best_result["accuracy"],
        "macro_f1": best_result["macro_f1"],
    }
    write_report(OUTPUT_DIR / "report.md", summary)

    print("数据集预览")
    print(f"- 原始游戏数: {len(rows)}")
    print(f"- 去重后游戏数: {len(clean_rows)}")
    print(f"- 最常见类型: {', '.join(top_genres[:5])}")
    print(f"- 最常见标签: {', '.join(top_tags[:5])}")
    print()
    print("KNN 训练结果")
    print(f"- best_k: {best_k}")
    print(f"- accuracy: {best_result['accuracy']:.4f}")
    print(f"- macro_f1: {best_result['macro_f1']:.4f}")
    print()
    print("输出文件已生成到 outputs/ 目录")


if __name__ == "__main__":
    main()
