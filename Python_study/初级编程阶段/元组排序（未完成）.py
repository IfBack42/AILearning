# 试题描述： 假设有一个学生信息列表，每个元素包含学生姓名、年龄和成绩。请按照以下要求完成操作：
#
# 使用 reverse() 方法将列表反转。
# 使用 sort() 方法按照成绩从高到低对列表进行排序。
# 输出平均年龄和前三名学生的信息（姓名、年龄和成绩）。
# 提示：如果列表里面嵌套了元祖，需要依据元祖中的元素，对列表进行排序，可以参考如下代码
#
# # 学生信息列表
# students = [('Alice', 20, 85), ('Bob', 19, 92), ('Catherine', 21, 78), ('David', 20, 95), ('Emily', 19, 88)]
#
# # 获取student中的第三个元素，例如：('Alice', 20, 85)获取85，('David', 20, 95)获取95
# def get_score(student):
#     return student[2]
#
# # 此行代码用于获取students列表中每一个student元素，并且使用get_score将每一个student中的得分拎出来，进# 行排序
# students.sort(key=get_score, reverse=True)
students = [('Alice', 20, 85), ('Bob', 19, 92), ('Catherine', 21, 78), ('David', 20, 95), ('Emily', 19, 88)]
students = list(students.__reversed__())
print(students)
# 以成绩给学生牌序，用擂台法，先获取学生成绩的元素再循环比较
ace = 0
max1 = students[0][2]
for i in students:
    if i[2] > max1:
        max1 = i[2]
        ace = i
print(students,max1,ace)
# 这里把大哥打出来了，但是前三不行，需要进行排序先
students.sort(students[2],True)