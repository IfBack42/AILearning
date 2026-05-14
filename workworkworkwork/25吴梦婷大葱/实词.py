import os
import re
import math
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


def process_files(folder_path, end_index):
    """处理所有文件"""
    all_content_words = []  # 所有内容的实词
    content_word_counts = []  # 每个内容的实词数量

    # 处理每个文件
    for i in range(0, end_index + 1):
        filename = f"reddit_content_{i}.txt"
        filepath = os.path.join(folder_path, filename)

        if not os.path.exists(filepath):
            print(f"文件 {filename} 不存在，跳过")
            continue

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

            # 提取内容部分
            extracted_content = extract_content(content)

            # 处理文本并获取实词
            content_words = process_text(extracted_content)

            # 收集数据
            all_content_words.extend(content_words)
            content_word_counts.append(len(content_words))

    return all_content_words, content_word_counts


def calculate_statistics(values):
    """计算统计信息"""
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


# 主程序
if __name__ == "__main__":
    folder_path = input("请输入文件夹路径: ")
    end_index = int(input("请输入结束编号: "))

    # 处理所有文件
    all_words, word_counts = process_files(folder_path, end_index)

    # 计算实词数量的统计信息
    word_count_stats = calculate_statistics(word_counts)

    # 计算实词频率统计
    word_freq = Counter(all_words)
    top_words = word_freq.most_common(20)

    # 输出结果
    print("\n内容实词数量统计:")
    if word_count_stats:
        print(f"处理文件数量: {word_count_stats['count']}")
        print(f"最小实词数: {word_count_stats['min']}")
        print(f"最大实词数: {word_count_stats['max']}")
        print(f"平均实词数: {word_count_stats['mean']:.2f}")
        print(f"中位数实词数: {word_count_stats['median']}")
        print(f"实词数标准差: {word_count_stats['std_dev']:.2f}")
    else:
        print("没有有效数据")

    print("\n最常见实词TOP 20:")
    for word, freq in top_words:
        print(f"{word}: {freq}次")

    # 保存完整词频统计
    output_file = os.path.join(folder_path, "word_frequency_report.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("完整词频统计报告:\n")
        f.write("=" * 50 + "\n")
        for word, freq in word_freq.most_common():
            f.write(f"{word}: {freq}\n")

    print(f"\n完整词频报告已保存至: {output_file}")