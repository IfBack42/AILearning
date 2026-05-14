import os
import re
import math
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter

# 下载NLTK资源（如果未安装）
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("下载NLTK资源...")
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')


def extract_game_stats(text):
    """提取游戏统计数据"""
    stats = {}

    # 提取游戏名称
    name_match = re.search(r"游戏名称:\s*(.+)", text)
    if name_match:
        stats["game_name"] = name_match.group(1).strip()

    # 提取App ID
    appid_match = re.search(r"App ID:\s*(\d+)", text)
    if appid_match:
        stats["app_id"] = appid_match.group(1)

    # 提取好评数
    positive_match = re.search(r"好评数:\s*(\d+)", text)
    if positive_match:
        stats["positive_reviews"] = int(positive_match.group(1))

    # 提取差评数
    negative_match = re.search(r"差评数:\s*(\d+)", text)
    if negative_match:
        stats["negative_reviews"] = int(negative_match.group(1))

    # 提取好评率
    rate_match = re.search(r"好评率:\s*([\d.]+)%", text)
    if rate_match:
        stats["positive_rate"] = float(rate_match.group(1))
    else:
        # 尝试从好评数和总评价数计算好评率
        if "positive_reviews" in stats and "total_reviews" in stats and stats["total_reviews"] > 0:
            stats["positive_rate"] = (stats["positive_reviews"] / stats["total_reviews"]) * 100

    # 提取总评价数
    total_match = re.search(r"总评价数:\s*(\d+)", text)
    if total_match:
        stats["total_reviews"] = int(total_match.group(1))
    else:
        # 如果没有总评价数，从好评和差评计算
        if "positive_reviews" in stats and "negative_reviews" in stats:
            stats["total_reviews"] = stats["positive_reviews"] + stats["negative_reviews"]

    # 提取数据获取时间
    time_match = re.search(r"数据获取时间:\s*(.+)", text)
    if time_match:
        stats["data_time"] = time_match.group(1).strip()

    return stats


def extract_comments(text):
    """提取所有评论内容"""
    comments = []

    # 使用正则表达式匹配评论内容
    comment_matches = re.findall(
        r"评论内容:\s*(.+?)(?=\n\s*--------------------------------------------------------------------------------|\Z)",
        text, re.DOTALL)

    for comment in comment_matches:
        # 清理评论内容：移除多余空格和换行
        cleaned_comment = " ".join(comment.strip().split())
        comments.append(cleaned_comment)

    return comments


def calculate_statistics(values):
    """计算统计指标"""
    if not values:
        return None

    n = len(values)
    values.sort()

    min_val = min(values)
    max_val = max(values)
    mean = sum(values) / n

    # 中位数
    if n % 2 == 1:
        median = values[n // 2]
    else:
        median = (values[n // 2 - 1] + values[n // 2]) / 2

    # 标准差
    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0

    return {
        "min": min_val,
        "max": max_val,
        "mean": mean,
        "median": median,
        "std_dev": std_dev,
        "count": n
    }


def analyze_word_statistics(comments):
    """分析评论内容的词频统计"""
    all_words = []

    # 处理文本内容
    for comment in comments:
        # 转换为小写
        content = comment.lower()

        # 移除特殊字符和标点
        content = re.sub(r'[^\w\s]', '', content)

        # 分词
        words = word_tokenize(content)

        # 加载停用词
        stop_words = set(stopwords.words('english'))

        # 词形还原
        lemmatizer = WordNetLemmatizer()

        # 过滤停用词并词形还原
        content_words = [
            lemmatizer.lemmatize(word)
            for word in words
            if word.isalpha() and word not in stop_words and len(word) > 2
        ]

        all_words.extend(content_words)

    # 计算词频
    word_freq = Counter(all_words)
    top_words = word_freq.most_common(20)

    # 计算每个评论的平均单词数
    comment_word_counts = [len(word_tokenize(comment)) for comment in comments]
    word_count_stats = calculate_statistics(comment_word_counts)

    # 计算每个评论的平均字符数
    comment_char_counts = [len(comment) for comment in comments]
    char_count_stats = calculate_statistics(comment_char_counts)

    return {
        "word_frequency": word_freq,
        "top_words": top_words,
        "word_count_stats": word_count_stats,
        "char_count_stats": char_count_stats
    }


def process_files(input_folder, output_folder):
    """处理文件夹中的所有文件"""
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 准备保存所有评论的文件
    all_comments_file = os.path.join(output_folder, "reddit_content_1822.txt")

    # 存储所有游戏的统计信息
    all_game_stats = []

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_folder, filename)

            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

                # 提取游戏统计数据
                game_stats = extract_game_stats(content)

                # 添加文件名信息
                game_stats["source_file"] = filename

                # 添加到游戏统计列表
                all_game_stats.append(game_stats)

                # 提取评论内容
                comments = extract_comments(content)

                # 保存评论到总评论文件
                with open(all_comments_file, 'a', encoding='utf-8') as comments_file:
                    for comment in comments:
                        comments_file.write(comment + "\n")

                print(f"处理完成: {filename}")

    # 计算跨游戏的统计信息
    positive_reviews = [g.get("positive_reviews", 0) for g in all_game_stats]
    negative_reviews = [g.get("negative_reviews", 0) for g in all_game_stats]
    total_reviews = [g.get("total_reviews", 0) for g in all_game_stats]
    positive_rates = [g.get("positive_rate", 0) for g in all_game_stats]

    # 计算统计数据
    game_stats_summary = {
        "positive_reviews": calculate_statistics(positive_reviews),
        "negative_reviews": calculate_statistics(negative_reviews),
        "total_reviews": calculate_statistics(total_reviews),
        "positive_rates": calculate_statistics(positive_rates),
        "game_count": len(all_game_stats)
    }

    # 保存游戏统计汇总
    game_stats_file = os.path.join(output_folder, "game_stats_summary.txt")
    with open(game_stats_file, 'w', encoding='utf-8') as summary_file:
        summary_file.write("===== 游戏评价统计汇总 =====\n")
        summary_file.write(f"分析的游戏数量: {game_stats_summary['game_count']}\n\n")

        # 写入好评统计
        if game_stats_summary["positive_reviews"]:
            stats = game_stats_summary["positive_reviews"]
            summary_file.write("=== 好评数统计 ===\n")
            summary_file.write(f"最小值: {stats['min']}\n")
            summary_file.write(f"最大值: {stats['max']}\n")
            summary_file.write(f"平均值: {stats['mean']:.2f}\n")
            summary_file.write(f"中位数: {stats['median']}\n")
            summary_file.write(f"标准差: {stats['std_dev']:.2f}\n\n")

        # 写入差评统计
        if game_stats_summary["negative_reviews"]:
            stats = game_stats_summary["negative_reviews"]
            summary_file.write("=== 差评数统计 ===\n")
            summary_file.write(f"最小值: {stats['min']}\n")
            summary_file.write(f"最大值: {stats['max']}\n")
            summary_file.write(f"平均值: {stats['mean']:.2f}\n")
            summary_file.write(f"中位数: {stats['median']}\n")
            summary_file.write(f"标准差: {stats['std_dev']:.2f}\n\n")

        # 写入总评价统计
        if game_stats_summary["total_reviews"]:
            stats = game_stats_summary["total_reviews"]
            summary_file.write("=== 总评价数统计 ===\n")
            summary_file.write(f"最小值: {stats['min']}\n")
            summary_file.write(f"最大值: {stats['max']}\n")
            summary_file.write(f"平均值: {stats['mean']:.2f}\n")
            summary_file.write(f"中位数: {stats['median']}\n")
            summary_file.write(f"标准差: {stats['std_dev']:.2f}\n\n")

        # 写入好评率统计
        if game_stats_summary["positive_rates"]:
            stats = game_stats_summary["positive_rates"]
            summary_file.write("=== 好评率统计 ===\n")
            summary_file.write(f"最小值: {stats['min']:.2f}%\n")
            summary_file.write(f"最大值: {stats['max']:.2f}%\n")
            summary_file.write(f"平均值: {stats['mean']:.2f}%\n")
            summary_file.write(f"中位数: {stats['median']:.2f}%\n")
            summary_file.write(f"标准差: {stats['std_dev']:.2f}\n")

    # 分析评论内容的词频
    # 首先读取之前保存的所有评论
    with open(all_comments_file, 'r', encoding='utf-8') as comments_file:
        all_comments = comments_file.readlines()
        # 移除行尾换行符
        all_comments = [c.strip() for c in all_comments if c.strip()]

    # 进行词频分析
    word_stats = analyze_word_statistics(all_comments)

    # 保存词频统计结果
    word_stats_file = os.path.join(output_folder, "word_stats_summary.txt")
    with open(word_stats_file, 'w', encoding='utf-8') as word_file:
        word_file.write("===== 评论词频统计汇总 =====\n")
        word_file.write(f"分析的评论数量: {len(all_comments)}\n\n")

        # 写入评论长度统计
        if word_stats["word_count_stats"]:
            stats = word_stats["word_count_stats"]
            word_file.write("=== 评论长度统计 (单词数) ===\n")
            word_file.write(f"最小值: {stats['min']}\n")
            word_file.write(f"最大值: {stats['max']}\n")
            word_file.write(f"平均值: {stats['mean']:.2f}\n")
            word_file.write(f"中位数: {stats['median']}\n")
            word_file.write(f"标准差: {stats['std_dev']:.2f}\n\n")

        if word_stats["char_count_stats"]:
            stats = word_stats["char_count_stats"]
            word_file.write("=== 评论长度统计 (字符数) ===\n")
            word_file.write(f"最小值: {stats['min']}\n")
            word_file.write(f"最大值: {stats['max']}\n")
            word_file.write(f"平均值: {stats['mean']:.2f}\n")
            word_file.write(f"中位数: {stats['median']}\n")
            word_file.write(f"标准差: {stats['std_dev']:.2f}\n\n")

        # 写入最常见单词
        if word_stats["top_words"]:
            word_file.write("=== 最常见20个单词 ===\n")
            for word, freq in word_stats["top_words"]:
                word_file.write(f"{word}: {freq}\n")

        # 保存完整词频统计
        word_file.write("\n\n===== 完整词频统计 =====")
        for word, freq in word_stats["word_frequency"].most_common():
            word_file.write(f"\n{word}: {freq}")

    # 返回处理结果
    return {
        "games_processed": len(all_game_stats),
        "comments_processed": len(all_comments),
        "game_stats": game_stats_summary,
        "word_stats": word_stats
    }


# 主程序
if __name__ == "__main__":
    input_folder = input("请输入包含原始文件的文件夹路径: ")
    output_folder = input("请输入输出文件夹路径: ")

    results = process_files(input_folder, output_folder)

    print("\n所有文件处理完成！")
    print(f"已处理 {results['games_processed']} 个游戏的 {results['comments_processed']} 条评论")
    print(f"游戏数据统计汇总已保存到: {os.path.join(output_folder, 'game_stats_summary.txt')}")
    print(f"评论内容分析汇总已保存到: {os.path.join(output_folder, 'word_stats_summary.txt')}")
    print(f"所有评论内容已保存到: {os.path.join(output_folder, 'reddit_content_1822.txt')}")