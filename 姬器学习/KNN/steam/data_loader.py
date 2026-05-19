import json


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
    """把空值转成空字符串，并去掉文本前后的多余空格。"""
    if value is None:
        return ""
    return str(value).strip()


def decode_index_list(indexes, names):
    """把 JSON 里的数字索引列表，还原成对应的类型名或标签名。"""
    decoded = []
    for item in indexes or []:
        if isinstance(item, int) and 0 <= item < len(names):
            decoded.append(names[item])
    return decoded


def load_games(path):
    """读取 Steam JSON 数据，并把每条游戏记录整理成字典格式。"""
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
