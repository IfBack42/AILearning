# """
# 代码使用 input() 函数接收用户输入的操作类型，并根据操作类型执行相应的操作。
#
# 如果操作类型为 "add"，代码会提示用户输入要添加的元素，并将其作为整数添加到集合中，然后输出更新后的集合。
# 如果操作类型为 "remove"，代码会提示用户输入要删除的元素，并将其从集合中删除，然后输出更新后的集合。
# 如果操作类型为 "update"，添加[5, 6]至列表中，最终展示为{1, 2, 3, 4, 5, 6}。
# 如果操作类型为 "search"，代码会提示用户输入要查找的元素，并判断集合中是否存在该元素，然后输出判断结果（True 或 False）。
# """
# from os import remove
#
# set_a = set()
# users = input("干嘛")
# if users == "add":
#     add_ = input("加啥？")
#     set_a = set_a.add(f"{add_}")
#     print(set_a)
# elif users == remove:
#     remove(f"{input("删谁？")}")
#     print(set_a)
# elif users == "update":
#     set_a.update([5,6])
#     print(set_a)
# elif users == "search":
#     who = input("要查的名字？")
#     if who in set_a:
#         print("True")
#     else:
#         print("False")


# 定义函数findall，要求返回符合要求的所有位置的起始下标，
# 如字符串"helloworldhellopythonhelloc++hellojava"需要找出里面所有的"hello"的位置
# ，返回的格式是一个元组，即：(0,10,21,29)
def findall(str_):
    list_ = []
    i = 0
    # 使用循环来查找“hello”下标并将其下标加入列表
    while True:
        i = str_.find("hello",i)
        if i == -1:
            break
        else:
            list_.append(i)
            i += 1
    return tuple(list_)


print(findall("helloworldhellopythonhelloc++hellojava"))
