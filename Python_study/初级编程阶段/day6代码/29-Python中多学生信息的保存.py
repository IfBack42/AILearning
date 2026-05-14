# 定义一个大列表
students = [{'name':'张三', 'age':23, 'mobile': '10086'}]
for i in students:
    i['name'] = '李四'

print(students)