# 6、定义一个全局列表，用于保存所有学员信息
students = []

# 1、定义一个menu函数，用于显示功能菜单
def menu():
    print('-' * 40)
    print('学生管理系统 V1.0')
    print('[1] 添加学生信息')
    print('[2] 删除学生信息')
    print('[3] 修改学生信息')
    print('[4] 查询学生信息')
    print('[5] 遍历所有学生信息')
    print('[6] 退出系统')
    print('-' * 40)

# 5、定义一个add_student函数，用于添加学生信息
def add_student():
    # 接收要输入学生的信息
    name = input('请输入要添加学生的姓名：')
    age = int(input('请输入要添加学生的年龄：'))
    mobile = input('请输入要添加学生的电话：')
    # 创建一个空字典
    student = {}
    student['name'] = name
    student['age'] = age
    student['mobile'] = mobile
    # 声明全局列表
    global students
    students.append(student)
    print(f'学生{name}信息添加成功')

# 7、定义一个get_all_students函数，用于获取所有学生信息
def get_all_students():
    # 声明全局变量
    global students
    # 遍历所有学员信息
    for i in students:
        print(i)

# 8、定义一个del_student函数，用于删除指定的学员信息
def del_student():
    # 提示用户输入要删除学生的姓名
    name = input('请输入要删除学生的姓名：')
    # 遍历所有学员，查看是否有某个学员的name(key)与输入的name值相匹配
    global students
    for i in students:
        if i['name'] == name:
            students.remove(i)
            print(f'学生{name}信息删除成功')
            break
    else:
        print('您要删除的学生信息未找到！')

# 9、定义一个edit_student函数，用于编辑学员的信息
def edit_student():
    # 提示用户输入要编辑学生的姓名
    name = input('请输入要编辑学生的姓名：')
    # 声明全局变量
    global students
    for i in students:
        if i['name'] == name:
            # 提示用户输入要修改的信息
            i['name'] = input('请输入修改后的学生姓名：')
            i['age'] = int(input('请输入修改后的学生年龄：'))
            i['mobile'] = input('请输入修改后的学生电话：')
            # 提示修改成功，然后break
            print(f'学生{name}信息已修改成功')
            break
    else:
        print('您要修改的学员未找到')

# 10、定义一个get_student函数，用于查询某个学员信息
def get_student():
    # 提示用户输入要查询学员的姓名
    name = input('请输入要查询学生的姓名：')
    # 声明全局变量，然后循环遍历
    global students
    for i in students:
        if i['name'] == name:
            # 找到了这个学员
            print(i)
            break
    else:
        print('您要查询的学生信息暂未找到')

# 2、定义一个死循环，用于让系统一直处于运行状态
while True:
    # 调用menu()菜单函数
    menu()
    # 3、提示用户输入要操作的功能编号
    user_num = int(input('请输入您要操作的功能编号：'))
    # 4、根据用户输入功能编号实现对应的功能
    if user_num == 1:
        # 添加学生信息
        add_student()
    elif user_num == 2:
        # 删除学生信息
        del_student()
    elif user_num == 3:
        # 修改学生信息
        edit_student()
    elif user_num == 4:
        # 查询学生信息
        get_student()
    elif user_num == 5:
        # 遍历所有学生的信息
        get_all_students()
    elif user_num == 6:
        # 退出系统
        print('退出系统成功，感谢您使用学生管理系统V1.0')
        break
    else:
        # 输入异常
        print('您输入的功能编号不正确，请重新输入')