import math
import random
from collections import Counter, defaultdict

from config import CURRENT_YEAR, RANDOM_SEED


def deduplicate_games(rows):
    """对重复游戏去重，同名同开发商时保留评论数最多的记录。"""
    best = {}
    for row in rows:
        key = (row["name"].casefold(), row["developer"].casefold())
        if key not in best or row["review_count"] > best[key]["review_count"]:
            best[key] = row
    return list(best.values())


def rating_group(rating_index):
    """把原始细粒度口碑等级合并成更适合课程项目的四个大类。"""
    if rating_index <= 1:
        return "highly_positive"
    if rating_index <= 3:
        return "positive"
    if rating_index == 4:
        return "mixed"
    return "negative"


def top_values(rows, field, n):
    """统计某个列表字段中出现次数最多的前 n 个值。"""
    counts = Counter()
    for row in rows:
        counts.update(row[field])
    return [name for name, _ in counts.most_common(n)]


def add_features(rows, top_genres, top_tags):
    """为每条游戏构造机器学习可用的数值特征和目标标签。"""
    developer_counts = Counter(row["developer"] for row in rows)
    featured = []

    for row in rows:
        genre_set = set(row["genres"])
        tag_set = set(row["tags"])
        item = {
            "name": row["name"],
            "developer": row["developer"],
            "release_year": int(row["release_year"]),
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


def stratified_sample(rows, max_size):
    """按类别比例抽样，避免某个口碑类别在样本中过多或过少。"""
    if len(rows) <= max_size:
        return list(rows)

    rnd = random.Random(RANDOM_SEED)
    by_class = defaultdict(list)
    for row in rows:
        by_class[row["target"]].append(row)

    sampled = []
    total = len(rows)
    for items in by_class.values():
        quota = max(1, round(max_size * len(items) / total))
        sampled.extend(rnd.sample(items, min(quota, len(items))))

    rnd.shuffle(sampled)
    return sampled[:max_size]


def train_test_split(rows, test_ratio=0.2):
    """按类别分层划分训练集和测试集，让测试集更有代表性。"""
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
