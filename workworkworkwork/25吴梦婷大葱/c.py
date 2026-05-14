import os
import re
import math
import json
import datetime
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

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


def extract_tweet_data(text):
    """提取推文数据"""
    tweet_data = {}

    # 提取发布时间
    time_match = re.search(r"发布时间:\s*(\d{4}-\d{2}-\d{2})T", text)
    if time_match:
        tweet_data["date"] = datetime.datetime.strptime(time_match.group(1), "%Y-%m-%d").date()

    # 提取点赞数、评论数和订阅数
    upvotes_match = re.search(r"点赞数:\s*(\d+)", text)
    comments_match = re.search(r"评论数:\s*(\d+)", text)
    subscriptions_match = re.search(r"订阅数:\s*(\d+)", text)

    tweet_data["upvotes"] = int(upvotes_match.group(1)) if upvotes_match else 0
    tweet_data["comments"] = int(comments_match.group(1)) if comments_match else 0
    tweet_data["subscriptions"] = int(subscriptions_match.group(1)) if subscriptions_match else 0

    return tweet_data


def extract_content(text):
    """提取内容部分"""
    # 找到内容部分的起始位置
    content_start = text.find("内容:")
    if content_start == -1:
        return ""

    # 找到内容部分的结束位置（下一个分割线）
    content_end = text.find("------------------------------------------------------------", content_start)
    if content_end == -1:
        content_end = len(text)

    # 提取内容文本
    content = text[content_start + 3:content_end].strip()
    return content


def extract_comments(text):
    """提取所有评论数据"""
    comments = []

    # 分割所有评论块
    comment_blocks = re.split(r'-{60}\n用户:', text)

    for block in comment_blocks[1:]:  # 跳过第一部分（推文内容）
        comment_data = {}

        # 提取用户名
        username_match = re.search(r'^(\w+)', block)
        if username_match:
            comment_data["user"] = username_match.group(1)

        # 提取点赞数
        upvotes_match = re.search(r"点赞:\s*(\d+)", block)
        comment_data["upvotes"] = int(upvotes_match.group(1)) if upvotes_match else 0

        # 提取时间
        time_match = re.search(r"时间:\s*(\d{4}-\d{2}-\d{2})T", block)
        if time_match:
            comment_data["date"] = datetime.datetime.strptime(time_match.group(1), "%Y-%m-%d").date()

        # 提取内容
        content_match = re.search(r"内容:\s*(.+?)(?=\n\s*$)", block, re.DOTALL)
        if content_match:
            comment_data["content"] = content_match.group(1).strip()

        comments.append(comment_data)

    return comments


def process_text(content):
    """处理文本内容并返回实词列表"""
    if not content:
        return []

    # 转换为小写
    content = content.lower()

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

    return content_words


def calculate_statistics(values):
    """计算数值统计信息"""
    if not values:
        return None

    n = len(values)
    values.sort()

    min_val = min(values)
    max_val = max(values)
    mean = sum(values) / n
    median = values[n // 2] if n % 2 == 1 else (values[n // 2 - 1] + values[n // 2]) / 2

    # 计算标准差
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = math.sqrt(variance)

    return {
        "min": min_val,
        "max": max_val,
        "mean": mean,
        "median": median,
        "std_dev": std_dev,
        "count": n
    }


def calculate_date_statistics(dates):
    """计算日期统计信息"""
    if not dates:
        return None

    min_date = min(dates)
    max_date = max(dates)

    # 计算日期范围（天数）
    date_range = (max_date - min_date).days

    return {
        "min_date": min_date.strftime("%Y-%m-%d"),
        "max_date": max_date.strftime("%Y-%m-%d"),
        "date_range_days": date_range,
        "count": len(dates)
    }


def process_files(folder_path, end_index):
    """处理所有文件"""
    all_tweets = []
    all_comments = []
    all_content_words = []
    content_word_counts = []

    # 处理每个文件
    for i in range(0, end_index + 1):
        filename = f"reddit_content_{i}.txt"
        filepath = os.path.join(folder_path, filename)

        if not os.path.exists(filepath):
            print(f"文件 {filename} 不存在，跳过")
            continue

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()

            # 提取推文数据
            tweet_data = extract_tweet_data(text)
            if tweet_data:
                tweet_data["source_file"] = filename
                all_tweets.append(tweet_data)

            # 提取评论数据
            comments = extract_comments(text)
            for comment in comments:
                comment["source_file"] = filename
            all_comments.extend(comments)

            # 提取内容并处理
            extracted_content = extract_content(text)
            content_words = process_text(extracted_content)
            all_content_words.extend(content_words)
            content_word_counts.append(len(content_words))

    return {
        "tweets": all_tweets,
        "comments": all_comments,
        "content_words": all_content_words,
        "word_counts": content_word_counts
    }


# 主程序
if __name__ == "__main__":
    folder_path = input("请输入文件夹路径: ")
    end_index = int(input("请输入结束编号: "))

    # 处理所有文件
    results = process_files(folder_path, end_index)

    # 计算推文统计数据
    tweet_dates = [tweet["date"] for tweet in results["tweets"] if "date" in tweet]
    tweet_upvotes = [tweet["upvotes"] for tweet in results["tweets"]]
    tweet_comments = [tweet["comments"] for tweet in results["tweets"]]
    tweet_subs = [tweet["subscriptions"] for tweet in results["tweets"]]

    tweet_date_stats = calculate_date_statistics(tweet_dates)
    tweet_upvote_stats = calculate_statistics(tweet_upvotes)
    tweet_comment_stats = calculate_statistics(tweet_comments)
    tweet_sub_stats = calculate_statistics(tweet_subs)

    # 计算评论统计数据
    comment_dates = [comment["date"] for comment in results["comments"] if "date" in comment]
    comment_upvotes = [comment["upvotes"] for comment in results["comments"]]

    comment_date_stats = calculate_date_statistics(comment_dates)
    comment_upvote_stats = calculate_statistics(comment_upvotes)

    # 计算内容实词统计数据
    word_count_stats = calculate_statistics(results["word_counts"])

    # 计算实词频率统计
    word_freq = Counter(results["content_words"])
    top_words = word_freq.most_common(20)

    # 输出结果
    print("\n===== 推文统计 =====")
    if tweet_date_stats:
        print(f"\n推文日期统计:")
        print(f"  最早推文日期: {tweet_date_stats['min_date']}")
        print(f"  最晚推文日期: {tweet_date_stats['max_date']}")
        print(f"  日期范围: {tweet_date_stats['date_range_days']} 天")

    if tweet_upvote_stats:
        print(f"\n推文点赞统计:")
        print(f"  最小点赞数: {tweet_upvote_stats['min']}")
        print(f"  最大点赞数: {tweet_upvote_stats['max']}")
        print(f"  平均点赞数: {tweet_upvote_stats['mean']:.2f}")
        print(f"  中位数点赞数: {tweet_upvote_stats['median']}")
        print(f"  点赞数标准差: {tweet_upvote_stats['std_dev']:.2f}")

    if tweet_comment_stats:
        print(f"\n推文评论统计:")
        print(f"  最小评论数: {tweet_comment_stats['min']}")
        print(f"  最大评论数: {tweet_comment_stats['max']}")
        print(f"  平均评论数: {tweet_comment_stats['mean']:.2f}")
        print(f"  中位数评论数: {tweet_comment_stats['median']}")
        print(f"  评论数标准差: {tweet_comment_stats['std_dev']:.2f}")

    if tweet_sub_stats:
        print(f"\n推文订阅统计:")
        print(f"  最小订阅数: {tweet_sub_stats['min']}")
        print(f"  最大订阅数: {tweet_sub_stats['max']}")
        print(f"  平均订阅数: {tweet_sub_stats['mean']:.2f}")
        print(f"  中位数订阅数: {tweet_sub_stats['median']}")
        print(f"  订阅数标准差: {tweet_sub_stats['std_dev']:.2f}")

    print("\n===== 评论统计 =====")
    if comment_date_stats:
        print(f"\n评论日期统计:")
        print(f"  最早评论日期: {comment_date_stats['min_date']}")
        print(f"  最晚评论日期: {comment_date_stats['max_date']}")
        print(f"  日期范围: {comment_date_stats['date_range_days']} 天")

    if comment_upvote_stats:
        print(f"\n评论点赞统计:")
        print(f"  最小点赞数: {comment_upvote_stats['min']}")
        print(f"  最大点赞数: {comment_upvote_stats['max']}")
        print(f"  平均点赞数: {comment_upvote_stats['mean']:.2f}")
        print(f"  中位数点赞数: {comment_upvote_stats['median']}")
        print(f"  点赞数标准差: {comment_upvote_stats['std_dev']:.2f}")

    print(f"\n评论总数: {len(results['comments'])}")
    print(f"每个推文平均评论数: {len(results['comments']) / len(results['tweets']):.2f}" if results[
        "tweets"] else "无推文数据")

    print("\n===== 内容统计 =====")
    if word_count_stats:
        print(f"\n内容实词数量统计:")
        print(f"  处理推文数量: {word_count_stats['count']}")
        print(f"  最小实词数: {word_count_stats['min']}")
        print(f"  最大实词数: {word_count_stats['max']}")
        print(f"  平均实词数: {word_count_stats['mean']:.2f}")
        print(f"  中位数实词数: {word_count_stats['median']}")
        print(f"  实词数标准差: {word_count_stats['std_dev']:.2f}")
    else:
        print("没有有效内容数据")

    print("\n最常见实词TOP 20:")
    for word, freq in top_words:
        print(f"{word}: {freq}次")

    # 保存完整报告
    report = {
        "tweets": {
            "date_stats": tweet_date_stats,
            "upvote_stats": tweet_upvote_stats,
            "comment_stats": tweet_comment_stats,
            "subscription_stats": tweet_sub_stats,
            "tweet_count": len(results["tweets"]),
            "tweets": results["tweets"]
        },
        "comments": {
            "date_stats": comment_date_stats,
            "upvote_stats": comment_upvote_stats,
            "comment_count": len(results["comments"]),
            "sample_comments": results["comments"][:10]  # 保存前10条评论作为样本
        },
        "content": {
            "word_count_stats": word_count_stats,
            "top_words": top_words,
            "total_words": len(results["content_words"])
        }
    }

    report_file = os.path.join(folder_path, "social_media_report.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n完整报告已保存至: {report_file}")