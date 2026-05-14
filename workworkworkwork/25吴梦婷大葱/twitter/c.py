import os
import re
from datetime import datetime
import numpy as np


def parse_file(file_path):
    """解析单个文件，提取推文和评论的统计信息"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取主推文信息
    tweet_likes = int(re.search(r'点赞数: (\d+)', content).group(1))
    tweet_comments = int(re.search(r'评论数: (\d+)', content).group(1))
    tweet_retweets = int(re.search(r'转发数: (\d+)', content).group(1))
    tweet_time = re.search(r'发布时间: (.+?)\n', content).group(1).strip()

    # 提取所有评论信息
    comments = []
    comment_blocks = re.split(r'=== 评论 ===', content)[1:]

    for block in comment_blocks:
        # 提取评论内容
        content_match = re.search(r'内容: (.+?)\n', block)
        comment_content = content_match.group(1).strip() if content_match else ""

        # 计算实词个数（非空格字符序列）
        word_count = len(re.findall(r'\S+', comment_content)) if comment_content else 0

        # 提取点赞数和时间
        likes_match = re.search(r'点赞数: (\d+)', block)
        time_match = re.search(r'发布时间: (.+?)\n', block)

        if likes_match and time_match:
            comments.append({
                'likes': int(likes_match.group(1)),
                'time': time_match.group(1).strip(),
                'word_count': word_count
            })

    return {
        'tweet': {
            'likes': tweet_likes,
            'comments': tweet_comments,
            'retweets': tweet_retweets,
            'time': tweet_time
        },
        'comments': comments
    }


def calculate_stats(values):
    """计算一组数值的统计指标"""
    if not values:
        return {
            'min': 0, 'max': 0, 'mean': 0, 'variance': 0,
            '25%': 0, '50%': 0, '75%': 0
        }

    arr = np.array(values)
    return {
        'min': np.min(arr),
        'max': np.max(arr),
        'mean': np.mean(arr),
        'variance': np.var(arr),
        '25%': np.percentile(arr, 25),
        '50%': np.median(arr),
        '75%': np.percentile(arr, 75)
    }


def calculate_time_stats(times):
    """计算时间相关的统计指标"""
    if not times:
        return {'min': None, 'max': None}

    # 转换时间格式
    datetime_objs = [datetime.strptime(t, "%a %b %d %H:%M:%S %z %Y") for t in times]
    return {
        'min': min(datetime_objs).strftime("%Y-%m-%d %H:%M:%S"),
        'max': max(datetime_objs).strftime("%Y-%m-%d %H:%M:%S")
    }


def process_folder(folder_path):
    """处理文件夹中的所有文件，计算统计信息"""
    tweet_likes = []
    tweet_comments = []
    tweet_retweets = []
    tweet_times = []

    comment_likes = []
    comment_word_counts = []
    comment_times = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            data = parse_file(file_path)

            # 收集推文数据
            tweet = data['tweet']
            tweet_likes.append(tweet['likes'])
            tweet_comments.append(tweet['comments'])
            tweet_retweets.append(tweet['retweets'])
            tweet_times.append(tweet['time'])

            # 收集评论数据
            for comment in data['comments']:
                comment_likes.append(comment['likes'])
                comment_word_counts.append(comment['word_count'])
                comment_times.append(comment['time'])

    # 计算推文统计信息
    tweet_stats = {
        'likes': calculate_stats(tweet_likes),
        'comments': calculate_stats(tweet_comments),
        'retweets': calculate_stats(tweet_retweets),
        'time': calculate_time_stats(tweet_times)
    }

    # 计算评论统计信息
    comment_stats = {
        'likes': calculate_stats(comment_likes),
        'word_count': calculate_stats(comment_word_counts),
        'time': calculate_time_stats(comment_times)
    }

    return {
        'tweet': tweet_stats,
        'comment': comment_stats
    }


def print_stats(stats):
    """格式化打印统计结果"""
    print("推文统计信息:")
    print(f"点赞数: 最小值={stats['tweet']['likes']['min']}, 最大值={stats['tweet']['likes']['max']}, "
          f"平均值={stats['tweet']['likes']['mean']:.2f}, 方差={stats['tweet']['likes']['variance']:.2f}")
    print(f"评论数: 最小值={stats['tweet']['comments']['min']}, 最大值={stats['tweet']['comments']['max']}, "
          f"平均值={stats['tweet']['comments']['mean']:.2f}, 方差={stats['tweet']['comments']['variance']:.2f}")
    print(f"转发数: 最小值={stats['tweet']['retweets']['min']}, 最大值={stats['tweet']['retweets']['max']}, "
          f"平均值={stats['tweet']['retweets']['mean']:.2f}, 方差={stats['tweet']['retweets']['variance']:.2f}")
    print(f"发布时间范围: {stats['tweet']['time']['min']} 至 {stats['tweet']['time']['max']}")

    print("\n评论统计信息:")
    print(f"点赞数: 最小值={stats['comment']['likes']['min']}, 最大值={stats['comment']['likes']['max']}, "
          f"平均值={stats['comment']['likes']['mean']:.2f}, 方差={stats['comment']['likes']['variance']:.2f}")
    print(f"实词个数: 最小值={stats['comment']['word_count']['min']}, 最大值={stats['comment']['word_count']['max']}, "
          f"平均值={stats['comment']['word_count']['mean']:.2f}, 方差={stats['comment']['word_count']['variance']:.2f}")
    print(f"发布时间范围: {stats['comment']['time']['min']} 至 {stats['comment']['time']['max']}")

    # 添加更详细的分布信息
    print("\n推文点赞数分布 (25%, 中位数, 75%): "
          f"{stats['tweet']['likes']['25%']}, {stats['tweet']['likes']['50%']}, {stats['tweet']['likes']['75%']}")
    print("评论实词个数分布 (25%, 中位数, 75%): "
          f"{stats['comment']['word_count']['25%']}, {stats['comment']['word_count']['50%']}, {stats['comment']['word_count']['75%']}")


if __name__ == "__main__":
    folder_path = "./data"  # 替换为包含数据文件的文件夹路径
    stats = process_folder(folder_path)
    print_stats(stats)