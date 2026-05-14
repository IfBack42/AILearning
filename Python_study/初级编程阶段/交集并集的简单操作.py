"""
使用 Python 编程语言编写一个程序，实现获取两个集合的交集和并集的功能。具体要求如下：

定义两个集合A和B，分别包含一些整数元素。
提示用户输入集合A的元素个数，并根据输入创建集合A。
提示用户逐个输入集合A的元素，并将其添加到集合A中。
同样地，提示用户输入集合B的元素个数，并根据输入创建集合B。
再次逐个提示用户输入集合B的元素，并将其添加到集合B中。
使用集合的交集操作，获取集合A和集合B的交集，并将结果存储在变量intersection中。
使用集合的并集操作，获取集合A和集合B的并集，并将结果存储在变量union中。
输出集合A和集合B的交集和并集的值。
"""
A = {1,2,3,4,5}
B = {2,3,4,5,6,7,7,8}
while True:
    users = input("A or B or break?")
    if users == "A":
        A.add(input("add na to A?"))
        continue
    if users == "B":
        B.add(input("add na to B?"))
        continue
    if users == "break":
        break
    else:
        print("瞎jb输入重来")
        continue
intersection = A & B
union = A | B
print(f"A与B的交集：{intersection}\nA与B的并集：{union}")