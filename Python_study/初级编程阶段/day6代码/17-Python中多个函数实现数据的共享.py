# 全局变量
students = []

def funcA():
    # 声明全局变量
    global students
    # 向全局变量中追加数据
    students.append(1)
    students.append(2)
    students.append(3)

def funcB():
    for i in students:
        print(i)


# 调用funcA函数，向列表中追加数据
funcA()
# 调用funcB函数
funcB()
