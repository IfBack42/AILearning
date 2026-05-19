from pathlib import Path


DATA_FILE = Path("steam_all_2005.json")
OUTPUT_DIR = Path("outputs")

CURRENT_YEAR = 2026
RANDOM_SEED = 42
SAMPLE_SIZE = 3500
TOP_GENRES = 10
TOP_TAGS = 12

K_VALUES = [1, 3, 5, 7, 9, 11, 15]

BASE_FEATURES = [
    "release_year",
    "game_age",
    "log_review_count",
    "price",
    "is_free",
    "genre_count",
    "tag_count",
    "developer_game_count",
]
