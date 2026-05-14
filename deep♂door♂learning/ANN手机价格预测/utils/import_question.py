import sys
import os

# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)
print("当前文件路径:", current_file)

# 获取当前文件所在目录 (src目录)
current_dir = os.path.dirname(current_file)
print("当前目录:", current_dir)

# 获取上一级目录 (项目根目录)
parent_dir = os.path.dirname(current_dir)
print("项目根目录:", parent_dir)

# 将项目根目录添加到 sys.path 的开头
sys.path.insert(0, parent_dir)
print("更新后的sys.path[0]:", sys.path[0])
