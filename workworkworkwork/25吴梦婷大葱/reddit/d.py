# 检查文件权限
import os
filename = "./reddit_content_1823/combined_comments.txt"
print(os.access(filename, os.W_OK))  # 检查是否可写

# 修改权限（需要管理员权限）
os.chmod(filename, 0o644)  # 设置为可写