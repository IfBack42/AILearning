import os
import re


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
    rate_match = re.search(r"好评率:\s*([\d.]+%)", text)
    if rate_match:
        stats["positive_rate"] = rate_match.group(1)

    # 提取总评价数
    total_match = re.search(r"总评价数:\s*(\d+)", text)
    if total_match:
        stats["total_reviews"] = int(total_match.group(1))

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


def process_files(input_folder, output_folder):
    """处理文件夹中的所有文件"""
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 准备保存所有评论的文件
    all_comments_file = os.path.join(output_folder, "reddit_content_1822.txt")

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_folder, filename)

            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

                # 提取游戏统计数据
                game_stats = extract_game_stats(content)

                # 提取评论内容
                comments = extract_comments(content)

                # 保存游戏统计数据到新文件
                stats_filename = f"stats_{filename}"
                stats_filepath = os.path.join(output_folder, stats_filename)

                with open(stats_filepath, 'w', encoding='utf-8') as stats_file:
                    stats_file.write("=== 游戏评价统计 ===\n")
                    for key, value in game_stats.items():
                        stats_file.write(f"{key}: {value}\n")

                # 保存评论到总评论文件
                with open(all_comments_file, 'a', encoding='utf-8') as comments_file:
                    for comment in comments:
                        comments_file.write(comment + "\n")

                print(f"处理完成: {filename}")


# 主程序
if __name__ == "__main__":
    input_folder = input("请输入包含原始文件的文件夹路径: ")
    output_folder = input("请输入输出文件夹路径: ")

    process_files(input_folder, output_folder)
    print("\n所有文件处理完成！")
    print(f"游戏统计数据已保存到 {output_folder} 文件夹")
    print(f"所有评论内容已保存到 {os.path.join(output_folder, 'reddit_content_1822.txt')}")