import os
import math
import datetime


def process_files(folder_path, end_index):
    dates = []
    upvotes_list = []
    comments_list = []
    subscriptions_list = []

    # 处理每个文件
    for i in range(0, end_index + 1):
        filename = f"reddit_content_{i}.txt"
        filepath = os.path.join(folder_path, filename)

        if not os.path.exists(filepath):
            print(f"文件 {filename} 不存在，跳过")
            continue

        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

            # 提取日期
            time_label = "发布时间:"
            time_index = content.find(time_label)
            if time_index != -1:
                time_line = content[time_index:].split('\n', 1)[0]
                time_str = time_line.replace(time_label, "").strip().split('T')[0]
                dates.append(datetime.datetime.strptime(time_str, "%Y-%m-%d").date())

            # 提取数值数据
            labels = ["点赞数:", "评论数:", "订阅数:"]
            lists = [upvotes_list, comments_list, subscriptions_list]

            for label, lst in zip(labels, lists):
                index = content.find(label)
                if index != -1:
                    data_line = content[index:].split('\n', 1)[0]
                    value = data_line.replace(label, "").strip()
                    if value.isdigit():
                        lst.append(int(value))

    # 计算日期范围
    min_date = min(dates) if dates else None
    max_date = max(dates) if dates else None

    # 计算统计数据
    def calculate_stats(data):
        if not data:
            return None
        data.sort()
        n = len(data)

        min_val = min(data)
        max_val = max(data)
        mean = sum(data) / n

        # 中位数计算
        median = data[n // 2] if n % 2 == 1 else (data[n // 2 - 1] + data[n // 2]) / 2

        # 标准差计算
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)

        return {
            "min": min_val,
            "max": max_val,
            "mean": mean,
            "median": median,
            "std_dev": std_dev
        }

    stats = {
        "upvotes": calculate_stats(upvotes_list),
        "comments": calculate_stats(comments_list),
        "subscriptions": calculate_stats(subscriptions_list)
    }

    return {
        "earliest_date": min_date,
        "latest_date": max_date,
        "stats": stats
    }


# 主程序
if __name__ == "__main__":
    folder_path = input("请输入文件夹路径: ")
    end_index = int(input("请输入结束编号: "))

    results = process_files(folder_path, end_index)

    print("\n日期统计:")
    print(f"最早日期: {results['earliest_date']}")
    print(f"最晚日期: {results['latest_date']}")

    print("\n数据统计:")
    for metric, stats in results['stats'].items():
        if stats:
            print(f"\n{metric.capitalize()}统计:")
            print(f"  最小值: {stats['min']}")
            print(f"  最大值: {stats['max']}")
            print(f"  平均值: {stats['mean']:.2f}")
            print(f"  中位数: {stats['median']}")
            print(f"  标准差: {stats['std_dev']:.2f}")
        else:
            print(f"\n{metric.capitalize()}无有效数据")