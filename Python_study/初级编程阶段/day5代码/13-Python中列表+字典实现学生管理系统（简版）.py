#  1、定义一个变量students，格式[{}, {}, {}]，用于保存班级中所有同学的信息
students = []

# 2、定义一个系统弹出功能菜单，告诉用户可以实现哪些功能
while True:
    print('-' * 40)
    print('欢迎使用传智播客.黑马程序员学生管理系统')
    print('[1]添加学生信息')
    print('[2]删除学生信息')
    print('[3]查询所有学生信息')
    print('[9]退出系统')
    print('-' * 40)

    usernum = int(input('请输入您要执行的功能编号：'))

    # 3、根据用户输入的编号执行相关的功能
    if usernum == 1:
        # 添加学生信息（name/age/mobile）
        name = input('请输入学生的姓名：')
        age = int(input('请输入学生的年龄：'))
        mobile = input('请输入学生的电话：')
        # 创建一个空字典
        student = {}
        student['name'] = name  # 字典名称[key] = value => student['name'] = '张士友'
        student['age'] = age
        student['mobile'] = mobile
        # 把student字典追加到students列表中
        students.append(student)
        print(f'学生信息{name}添加成功！')

    elif usernum == 2:
        # 删除学生信息
        name = input('请输入要删除学员的姓名：')
        # 对students进行遍历操作
        for i in students:
            if i['name'] == name:
                students.remove(i)
                print(f'学员信息{name}已被删除')
                break
        else:
            print('您要删除的学员信息未找到')

    elif usernum == 3:
        # 查询所有学生信息（只需要对students列表进行遍历即可）
        # students = [{}, {}, {}]
        for i in students:
            print(i)

    elif usernum == 9:
        print('系统退出成功，感谢使用传智播客.黑马程序员学生管理系统！')
        break


