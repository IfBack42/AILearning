import csv


def write_csv(path, rows, columns):
    """把列表字典数据写成 CSV 文件，方便用 Excel 查看。"""
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_report(path, summary):
    """根据训练结果生成一份 Markdown 格式的课程汇报稿。"""
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

## 7. 汇报时可以强调的困难

- 原始 JSON 不是标准表格，类型和标签需要先通过索引还原。
- 标签属于文本型、多值型特征，multi-hot 编码只能表示“是否出现”，不能理解标签之间的语义关系。
- 如果保留全部标签，特征会变得很稀疏，KNN 的距离效果会变差。
- 数据中可用特征偏少，很多真正影响口碑的因素没有记录。
- KNN 预测时计算量较大，所以本项目使用分层抽样控制运行时间。
"""
    path.write_text(text, encoding="utf-8")
