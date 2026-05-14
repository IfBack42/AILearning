import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


DATA_FILE = Path("steam_all_2005.json")
OUTPUT_DIR = Path("outputs")
CURRENT_YEAR = 2026
RANDOM_SEED = 42
SAMPLE_SIZE = 3500
TOP_GENRES = 10
TOP_TAGS = 12


GAME_COLUMNS = [
    "name",
    "release_year",
    "positive_rate",
    "review_count",
    "price",
    "rating_index",
    "genre_ids",
    "tag_ids",
    "developer",
]


def safe_text(value):
    if value is None:
        return ""
    return str(value).strip()


def decode_index_list(indexes, names):
    decoded = []
    for item in indexes or []:
        if isinstance(item, int) and 0 <= item < len(names):
            decoded.append(names[item])
    return decoded


def load_games(path):
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    ratings = raw["ratings"]
    genres = raw["genres"]
    tags = raw["tags"]
    rows = []
    for game in raw["games"]:
        record = dict(zip(GAME_COLUMNS, game))
        record["name"] = safe_text(record["name"])
        record["developer"] = safe_text(record["developer"]) or "Unknown"
        record["genres"] = decode_index_list(record["genre_ids"], genres)
        record["tags"] = decode_index_list(record["tag_ids"], tags)
        record["rating_name"] = ratings[record["rating_index"]]
        rows.append(record)
    return rows, ratings, genres, tags


def deduplicate_games(rows):
    """Keep the row with the largest review count for duplicated name/developer pairs."""
    best = {}
    for row in rows:
        key = (row["name"].casefold(), row["developer"].casefold())
        if key not in best or row["review_count"] > best[key]["review_count"]:
            best[key] = row
    return list(best.values())


def rating_group(rating_index):
    if rating_index <= 1:
        return "highly_positive"
    if rating_index <= 3:
        return "positive"
    if rating_index == 4:
        return "mixed"
    return "negative"


def add_features(rows, top_genres, top_tags):
    developer_counts = Counter(row["developer"] for row in rows)
    featured = []
    for row in rows:
        genre_set = set(row["genres"])
        tag_set = set(row["tags"])
        item = {
            "name": row["name"],
            "developer": row["developer"],
            "release_year": row["release_year"],
            "game_age": max(0, CURRENT_YEAR - int(row["release_year"])),
            "positive_rate": float(row["positive_rate"]),
            "review_count": int(row["review_count"]),
            "log_review_count": math.log1p(int(row["review_count"])),
            "price": float(row["price"]),
            "is_free": 1 if float(row["price"]) <= 0 else 0,
            "genre_count": len(row["genres"]),
            "tag_count": len(row["tags"]),
            "developer_game_count": developer_counts[row["developer"]],
            "rating_name": row["rating_name"],
            "target": rating_group(int(row["rating_index"])),
            "genres_text": "; ".join(row["genres"]),
            "tags_text": "; ".join(row["tags"]),
        }
        for genre in top_genres:
            item[f"genre_{genre}"] = 1 if genre in genre_set else 0
        for tag in top_tags:
            item[f"tag_{tag}"] = 1 if tag in tag_set else 0
        featured.append(item)
    return featured


def top_values(rows, field, n):
    counts = Counter()
    for row in rows:
        counts.update(row[field])
    return [name for name, _ in counts.most_common(n)]


def stratified_sample(rows, max_size):
    if len(rows) <= max_size:
        return list(rows)
    rnd = random.Random(RANDOM_SEED)
    by_class = defaultdict(list)
    for row in rows:
        by_class[row["target"]].append(row)

    sampled = []
    total = len(rows)
    for label, items in by_class.items():
        quota = max(1, round(max_size * len(items) / total))
        sampled.extend(rnd.sample(items, min(quota, len(items))))
    rnd.shuffle(sampled)
    return sampled[:max_size]


def train_test_split(rows, test_ratio=0.2):
    rnd = random.Random(RANDOM_SEED)
    by_class = defaultdict(list)
    for row in rows:
        by_class[row["target"]].append(row)

    train, test = [], []
    for items in by_class.values():
        rnd.shuffle(items)
        cut = max(1, int(len(items) * test_ratio))
        test.extend(items[:cut])
        train.extend(items[cut:])
    rnd.shuffle(train)
    rnd.shuffle(test)
    return train, test


def build_matrix(rows, feature_names):
    return [[float(row[name]) for name in feature_names] for row in rows]


def fit_scaler(matrix):
    columns = list(zip(*matrix))
    means = [sum(col) / len(col) for col in columns]
    stds = []
    for mean, col in zip(means, columns):
        variance = sum((x - mean) ** 2 for x in col) / len(col)
        std = math.sqrt(variance)
        stds.append(std if std > 1e-12 else 1.0)
    return means, stds


def transform(matrix, means, stds):
    return [[(x - mean) / std for x, mean, std in zip(row, means, stds)] for row in matrix]


def euclidean_squared(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def knn_predict_one(train_x, train_y, sample, k):
    distances = []
    for features, label in zip(train_x, train_y):
        distances.append((euclidean_squared(features, sample), label))
    distances.sort(key=lambda item: item[0])
    votes = Counter(label for _, label in distances[:k])
    return votes.most_common(1)[0][0]


def evaluate_knn(train_x, train_y, test_x, test_y, k):
    predictions = [knn_predict_one(train_x, train_y, row, k) for row in test_x]
    labels = sorted(set(train_y) | set(test_y))
    matrix = {actual: Counter() for actual in labels}
    correct = 0
    for actual, pred in zip(test_y, predictions):
        matrix[actual][pred] += 1
        correct += int(actual == pred)

    accuracy = correct / len(test_y)
    metrics = {}
    for label in labels:
        tp = matrix[label][label]
        fp = sum(matrix[other][label] for other in labels if other != label)
        fn = sum(matrix[label][other] for other in labels if other != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        metrics[label] = {"precision": precision, "recall": recall, "f1": f1}
    macro_f1 = sum(item["f1"] for item in metrics.values()) / len(metrics)
    return predictions, {"accuracy": accuracy, "macro_f1": macro_f1, "by_class": metrics, "matrix": matrix}


def write_csv(path, rows, columns):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def svg_bar_chart(path, title, labels, values, width=920, height=520, color="#3b82f6"):
    max_value = max(values) if values else 1
    left, right, top, bottom = 210, 40, 70, 50
    plot_w = width - left - right
    row_h = (height - top - bottom) / max(1, len(labels))
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="22" font-family="Arial" fill="#111827">{title}</text>',
    ]
    for i, (label, value) in enumerate(zip(labels, values)):
        y = top + i * row_h + 8
        bar_w = plot_w * value / max_value
        lines.append(f'<text x="{left-12}" y="{y+row_h*0.55:.1f}" text-anchor="end" font-size="13" font-family="Arial" fill="#374151">{label}</text>')
        lines.append(f'<rect x="{left}" y="{y}" width="{bar_w:.1f}" height="{max(14, row_h-12):.1f}" rx="4" fill="{color}"/>')
        lines.append(f'<text x="{left+bar_w+8:.1f}" y="{y+row_h*0.55:.1f}" font-size="12" font-family="Arial" fill="#111827">{value}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def svg_scatter(path, title, rows, width=920, height=560):
    left, right, top, bottom = 70, 40, 70, 70
    plot_w = width - left - right
    plot_h = height - top - bottom
    xs = [row["price"] for row in rows]
    ys = [row["positive_rate"] for row in rows]
    max_x = max(xs) if xs else 1
    colors = {
        "highly_positive": "#16a34a",
        "positive": "#2563eb",
        "mixed": "#f59e0b",
        "negative": "#dc2626",
    }
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="22" font-family="Arial" fill="#111827">{title}</text>',
        f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="#374151"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="#374151"/>',
        f'<text x="{left+plot_w/2}" y="{height-22}" text-anchor="middle" font-size="14" font-family="Arial">价格 Price</text>',
        f'<text x="22" y="{top+plot_h/2}" transform="rotate(-90 22 {top+plot_h/2})" text-anchor="middle" font-size="14" font-family="Arial">好评率 Positive Rate</text>',
    ]
    for row in rows:
        x = left + (row["price"] / max_x) * plot_w
        y = top + (1 - row["positive_rate"] / 100) * plot_h
        radius = min(8, 2 + math.log1p(row["review_count"]) / 3)
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{colors[row["target"]]}" fill-opacity="0.55"/>')
    legend_x = left + plot_w - 170
    for i, (label, color) in enumerate(colors.items()):
        y = top + i * 24
        lines.append(f'<circle cx="{legend_x}" cy="{y}" r="6" fill="{color}"/>')
        lines.append(f'<text x="{legend_x+12}" y="{y+5}" font-size="13" font-family="Arial" fill="#111827">{label}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_report(path, summary):
    text = f"""# Steam 游戏口碑 KNN 分类课程汇报

## 1. 项目目标

本项目使用 `steam_all_2005.json` 中的 Steam 游戏数据，训练一个 KNN 分类模型，根据游戏的年份、价格、评论数量、类型、标签、开发商历史作品数量等特征，预测游戏属于哪一种口碑等级。

为了避免“答案泄露”，模型没有把 `positive_rate` 和原始 `rating_index` 当作输入特征。它们只用于生成目标标签和可视化分析。

## 2. JSON 数据预览

原始 JSON 顶层字段包括：

- `ratings`：口碑等级名称表，例如 Very Positive、Mixed。
- `genres`：游戏类型名称表。
- `tags`：游戏标签名称表。
- `games`：真正的游戏记录，每条记录是一个列表。

`games` 每条记录的含义为：

`[游戏名, 发行年份, 好评率, 评论数, 价格, 口碑等级索引, 类型索引列表, 标签索引列表, 开发商]`

## 3. 数据预处理亮点

- 索引还原：把 `genre_ids`、`tag_ids` 从数字索引转换成可读名称。
- 去重处理：同一游戏和同一开发商重复出现时，保留评论数最多的一条。
- 缺失处理：开发商为空时填充为 `Unknown`。
- 特征工程：构造 `game_age`、`log_review_count`、`is_free`、`genre_count`、`tag_count`、`developer_game_count`。
- 多标签编码：选取出现频率最高的 {summary["top_genres"]} 个类型和 {summary["top_tags"]} 个标签，做 multi-hot 编码。
- 标准化：KNN 依赖距离计算，因此训练前对所有数值特征做 Z-score 标准化。
- 分层抽样：KNN 计算量较大，训练时从全量清洗数据中按类别比例抽样 {summary["sample_size"]} 条。

## 4. 目标标签

原始 `rating_index` 被合并成四类，降低课程项目难度：

- `highly_positive`：Overwhelmingly Positive / Very Positive
- `positive`：Mostly Positive / Positive
- `mixed`：Mixed
- `negative`：Mostly Negative 及更低

## 5. 模型结果

- 清洗前样本数：{summary["raw_count"]}
- 清洗后样本数：{summary["clean_count"]}
- 训练评估样本数：{summary["sample_size"]}
- 最优 K：{summary["best_k"]}
- 测试集 Accuracy：{summary["accuracy"]:.4f}
- 测试集 Macro-F1：{summary["macro_f1"]:.4f}

## 6. 输出文件

- `outputs/cleaned_sample.csv`：清洗后的样例数据。
- `outputs/metrics.csv`：不同 K 值的 Accuracy 和 Macro-F1。
- `outputs/confusion_matrix.csv`：最优 K 的混淆矩阵。
- `outputs/rating_distribution.svg`：口碑等级分布图。
- `outputs/top_genres.svg`：热门游戏类型图。
- `outputs/top_tags.svg`：热门标签图。
- `outputs/price_positive_scatter.svg`：价格与好评率散点图。

## 7. 课程汇报讲解思路

可以按“数据集结构 -> 预处理 -> 特征工程 -> KNN 原理 -> 实验结果 -> 可视化发现”的顺序讲。重点强调：KNN 很依赖特征尺度，所以标准化是必要步骤；原始 JSON 使用索引压缩存储，所以把索引还原为可解释字段，是本项目最重要的数据预处理环节。
"""
    path.write_text(text, encoding="utf-8")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    rows, _, _, _ = load_games(DATA_FILE)
    clean_rows = deduplicate_games(rows)

    top_genres = top_values(clean_rows, "genres", TOP_GENRES)
    top_tags = top_values(clean_rows, "tags", TOP_TAGS)
    featured = add_features(clean_rows, top_genres, top_tags)

    base_features = [
        "release_year",
        "game_age",
        "log_review_count",
        "price",
        "is_free",
        "genre_count",
        "tag_count",
        "developer_game_count",
    ]
    feature_names = base_features + [f"genre_{x}" for x in top_genres] + [f"tag_{x}" for x in top_tags]

    sample = stratified_sample(featured, SAMPLE_SIZE)
    train_rows, test_rows = train_test_split(sample)
    train_x = build_matrix(train_rows, feature_names)
    test_x = build_matrix(test_rows, feature_names)
    means, stds = fit_scaler(train_x)
    train_x = transform(train_x, means, stds)
    test_x = transform(test_x, means, stds)
    train_y = [row["target"] for row in train_rows]
    test_y = [row["target"] for row in test_rows]

    metrics_rows = []
    best = None
    for k in [1, 3, 5, 7, 9, 11, 15]:
        _, result = evaluate_knn(train_x, train_y, test_x, test_y, k)
        metrics_rows.append({"k": k, "accuracy": result["accuracy"], "macro_f1": result["macro_f1"]})
        if best is None or result["macro_f1"] > best[1]["macro_f1"]:
            best = (k, result)

    best_k, best_result = best
    labels = sorted(best_result["matrix"].keys())
    confusion_rows = []
    for actual in labels:
        row = {"actual": actual}
        for pred in labels:
            row[pred] = best_result["matrix"][actual][pred]
        confusion_rows.append(row)

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
