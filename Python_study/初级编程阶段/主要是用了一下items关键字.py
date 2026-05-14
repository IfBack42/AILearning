"""
假设你正在开发一个学生成绩管理系统，需要编写 Python 代码来计算每个学生的总成绩。请完成以下要求：

已知一个学生成绩字典 grades，包含多个学生的成绩信息。
其中，键是学生的姓名，值是该学生的成绩列表（整数型）。请使用函数嵌套调用的方式编写代码，实现以下功能：

创建一个函数 calculate_total_score(grades)，计算每个学生的总成绩，并返回一个字典，其中键是学生的姓名，值是该学生的总成绩。
在 calculate_total_score(grades)函数内部，通过调用一个名为calculate_student_score(grades)的函数来计算每个学生的总成绩。
该函数接受一个成绩列表作为参数，并返回该学生的总成绩。
在主程序中调用 calculate_total_score(grades) 函数，并输出每个学生的总成绩。
请编写上述要求的代码，并输出每个学生的总成绩。
学生成绩如下：

grades = {
    "Alice": [80, 90, 85, 95, 70],
    "Bob": [75, 60, 92, 88, 78],
    "Charlie": [90, 85, 88, 92, 95]
}
"""
grades = {
    "Alice": [80, 90, 85, 95, 70],
    "Bob": [75, 60, 92, 88, 78],
    "Charlie": [90, 85, 88, 92, 95]
}

def calculate_total_score(x):
    # 先用外层函数遍历每个学生的成绩再传入内层函数
    for key,value in x.items():
        global grades
        grades[key] = calculate_student_score(value)

def calculate_student_score(list_):
    #  使用内层函数计算学生总成绩
    sum_per_student = 0
    for i in list_:
        sum_per_student += i
    return sum_per_student

calculate_total_score(grades)
print(grades)


