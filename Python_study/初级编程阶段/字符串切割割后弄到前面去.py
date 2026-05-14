#假设您是一家在线图书店的开发者，需要编写程序来处理图书的标题。为了提高用户体验，需要对图书标题进行规范化处理。现在，需要你编写一段代码来处理图书标题，根据以下要求进行处理：

# 将标题中的所有单词的首字母大写。
# 如果标题以特定后缀结尾（例如 "Series"），将该后缀移到标题的开头，并添加冒号和一个空格。例如，"harry potter series" 应处理为 "Series: Harry Potter"。
# 输出处理后的标题。
# 示例：
#
# 输入：title = "harry potter series" 输出：处理后的标题为 "Series: Harry Potter"
#
# 提示：运用到的相关方法
while True:
    name = input("爷来帮你转换=>书名：")
    name = name.title()
    # 先分割字符串的末尾使其成为列表
    if name.endswith("Series"):
        name = name.split(" ")
        # 切割列表
        switch = name.pop()
        # 再修改列表，使其末尾加上冒号，再移动到字符串前方
        switch += "："
        name.insert(0, switch)
        name = " ".join(name)
        print(name)
    else:
        print("瞎几把输入我让你飞起来")
        continue
