import os
import re


def extract_comments_from_file(file_path):
    """从单个文件中提取评论内容"""
    comments = []

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # 使用正则表达式找到所有评论内容
        comment_sections = re.findall(
            r'评论列表:(.*?)(?=\n================================================================================|\Z)',
            content,
            re.DOTALL
        )

        if comment_sections:
            # 分割每条评论
            raw_comments = re.split(r'\n\s*\n', comment_sections[0].strip())

            for com in raw_comments:
                # 提取评论内容部分
                if '内容:' in com:
                    # 获取内容字段后的所有文本
                    comment_text = com.split('内容:', 1)[1].strip()
                    # 移除可能的换行符和多余空格
                    comment_text = ' '.join(comment_text.split())
                    comments.append(comment_text)

    return comments


def process_folder(input_folder, output_file):
    """处理整个文件夹并将结果写入输出文件"""
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for filename in os.listdir(input_folder):
            if filename.endswith('.txt'):  # 假设所有文档都是txt格式
                file_path = os.path.join(input_folder, filename)
                comments = extract_comments_from_file(file_path)

                for comment in comments:
                    out_f.write(comment + '\n')

                print(f"Processed {filename}, found {len(comments)} comments")


if __name__ == "__main__":
    # 配置路径
    input_folder = "./content"  # 替换为您的文件夹路径
    output_file = "comments.txt"  # 输出文件名

    process_folder(input_folder, output_file)
    print(f"所有评论已保存到 {output_file}")