"""
代码使用 input() 函数接收用户输入的操作类型，并根据操作类型执行相应的操作。

如果操作类型为 "add"，代码会提示用户输入要添加的元素，并将其作为整数添加到集合中，然后输出更新后的集合。
如果操作类型为 "remove"，代码会提示用户输入要删除的元素，并将其从集合中删除，然后输出更新后的集合。
如果操作类型为 "update"，添加[5, 6]至列表中，最终展示为{1, 2, 3, 4, 5, 6}。
如果操作类型为 "search"，代码会提示用户输入要查找的元素，并判断集合中是否存在该元素，然后输出判断结果（True 或 False）。
"""
from operator import index
from re import search

set_ = {1,2,3,4}
users = input()
if users == "add":
    set_.add(input("请输入要添加的元素："))
    print(set_)
elif users == "remove":
    set.remove(input("请输入你要删除的元素："))
    print(set_)
elif users == "update":
    set_.update([5,6])
    print(set_)
elif users == "search":
    element = eval(input("你要查找的元素："))
    print(element in set_)