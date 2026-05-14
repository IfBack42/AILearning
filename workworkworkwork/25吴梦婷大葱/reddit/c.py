import os
import re


def extract_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式匹配所有评论内容
    pattern = r'内容:\s*\n(.*?)(?=\n------------------------------------------------------------|\Z)'
    comments = re.findall(pattern, content, re.DOTALL)

    # 清理并处理评论内容
    cleaned_comments = []
    for comment in comments:
        # 移除多余的空行和尾部空白
        cleaned = comment.strip()
        # 将多行评论转换为单行（保留内部换行符）
        cleaned = cleaned.replace('\n', ' ')  # 可选：如果希望保留原始换行格式，移除此行
        if cleaned:
            cleaned_comments.append(cleaned)

    return cleaned_comments


def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):  # 仅处理文本文件
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_comments.txt")

            comments = extract_comments(input_path)

            with open(output_path, 'w', encoding='utf-8') as out_file:
                for comment in comments:
                    out_file.write(comment + '\n')

            print(f"Processed: {filename} -> Extracted {len(comments)} comments")


if __name__ == "__main__":
    input_folder = "./content"  # 替换为包含文档的文件夹路径
    output_folder = "extracted_comments"  # 替换为输出文件夹路径

    process_folder(input_folder, output_folder)