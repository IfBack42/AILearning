# Steam 游戏口碑 KNN 分类课程项目

这个项目用于课程汇报：读取 `steam_all_2005.json`，完成 JSON 数据预览、数据清洗、特征工程、可视化，并用 KNN 预测游戏口碑等级。

## 运行方法

```bash
python knn_steam_report.py
```

运行后会生成 `outputs/` 目录，里面包含：

- `report.md`：课程汇报文字稿。
- `cleaned_sample.csv`：清洗后的数据样例。
- `metrics.csv`：不同 K 值的评估结果。
- `confusion_matrix.csv`：混淆矩阵。
- `rating_distribution.svg`：口碑等级分布图。
- `top_genres.svg`：热门类型图。
- `top_tags.svg`：热门标签图。
- `price_positive_scatter.svg`：价格与好评率散点图。

## 模块结构

- `knn_steam_report.py`：主入口，负责串联完整训练流程。
- `config.py`：统一保存路径、随机种子、抽样数量、K 值等配置。
- `data_loader.py`：读取 JSON，并把类型、标签索引还原为可读文本。
- `preprocessing.py`：数据去重、目标标签合并、特征工程、分层抽样、训练集测试集划分。
- `model.py`：矩阵构建、标准化、KNN 预测、模型评估。
- `visualization.py`：生成 SVG 可视化图表。
- `reporting.py`：导出 CSV 和 Markdown 汇报文件。

## 项目亮点

1. 原始 JSON 使用数字索引压缩存储类型和标签，脚本会把索引还原成可读文本。
2. 对重复游戏做去重，保留评论数最多的一条。
3. 构造 `game_age`、`log_review_count`、`is_free`、`developer_game_count` 等特征。
4. 对多类型、多标签字段做 multi-hot 编码。
5. KNN 依赖距离，因此训练前做 Z-score 标准化。
6. 多个 K 值共用同一批邻居排序，避免重复计算距离，运行更快。
7. 不依赖 pandas、scikit-learn、matplotlib，核心训练和 SVG 图表都用 Python 标准库实现。

## 汇报建议

可以重点讲“为什么 KNN 需要标准化”和“为什么要把类型、标签这种列表字段转换成 multi-hot 特征”。同时说明 multi-hot 只是课程项目中的简化方案，它不能理解标签之间的语义关系，这是项目遇到的主要困难之一。
