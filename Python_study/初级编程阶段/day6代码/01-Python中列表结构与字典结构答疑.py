students = []  # 用于保存所有同学的信息
# [{}, {}, {}]

for i in range(2):
    name = input('请输入学员的名称：')
    age = int(input('请输入学员的年龄：'))
    mobile = input('请输入学员的电话：')

    student = {}
    student['name'] = name
    student['age'] = age
    student['mobile'] = mobile

    students.append(student)

print(students)