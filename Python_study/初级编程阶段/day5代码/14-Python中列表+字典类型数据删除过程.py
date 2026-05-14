# 定义一个列表
students = [{'name': '王世贤', 'age': 25, 'mobile': '10086'}, {'name': '李光华', 'age': 27, 'mobile': '10010'}]
# 提示用户输入要删除学员的姓名
name = input('请输入要删除学员的姓名：')  # 李光华
# 判断"李光华"是否在列表中
for i in students:
    # i = {'name':'李光华','age':27,'mobile':'10010'}
    if i['name'] == name:
        # 代表这个同学就是要删除的同学信息
        students.remove(i)
        print(f'学员信息{name}删除成功')
        break
else:
    print(f'您要删除的同学信息未找到')


# students = [{'name': '王世贤', 'age': 25, 'mobile': '10086'}, {'name': '李光华', 'age': 27, 'mobile': '10010'}]
# students.remove({'name': '李光华', 'age': 27, 'mobile': '10010'})
# print(students)