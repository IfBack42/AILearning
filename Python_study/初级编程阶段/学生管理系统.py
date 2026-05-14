students = []

# 开始界面
while True:
    print("-" * 40)
    print("""
    欢迎使用肖杰学生让你管理系统
    录入学生信息请扣 【1】
    删除学生信息请扣 【2】
    查询所有学生信息请扣 【3】
    退出使用请扣 【9】
    """)
    print("-" * 40)
    users = int(input())
    if users == 1:
        student_new = {} # 创建一个新字典
        name = input("请输入录入学生的名称：")
        gender = input("请输入录入学生的性别：")
        id = input("请输入录入学生的学号：")
        # 将录入的学生数据加入字典中
        student_new["name"] = name
        student_new["gender"] = gender
        student_new["id"] = id
        # 将新字典放入列表
        students.append(student_new)
        print(f"已成功录入学生{name}信息")
        continue
    if users == 2:
        name_del = input("请输入要删除的学生信息：")
        for i in students: # 判断students列表中字典元素中元素“name“
            if i["name"] == name_del:
                students.remove(i)
                print(f"已成功删除学生{name}信息")

        continue
    if users == 3:
        for i in students:
            print(i)
        continue
    if users == 9:
        break
    else:
        print("无效指令")
        continue

