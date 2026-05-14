"""
试题描述： 某个公司的员工信息以字典形式存储，键为员工的工号，值为包含姓名、年龄和职位的字典。现在，你需要编写一个程序来完成对员工信息的增删改查操作。

要求：

查询：根据给定的员工工号，从字典中查找对应员工的信息，并返回员工的姓名、年龄和职位。
增加：将给定的员工信息添加到字典中。
删除，根据给定的员工工号，从字典中删除对应的员工信息。
已知有如下员工：
employee_records['1001'] = {'name': 'Alice', 'age': 25, 'position': 'Manager'}
employee_records['1002'] = {'name': 'Bob', 'age': 30, 'position': 'Engineer'}
"""
employee_records = {}
employee_records['1001'] = {'name': 'Alice', 'age': 25, 'position': 'Manager'}
employee_records['1002'] = {'name': 'Bob', 'age': 30, 'position': 'Engineer'}
print(employee_records)
print(employee_records.get(input("要查员工的工号")))
employee_add = {}
employee_add["name"] = input("添加的员工的姓名：")
employee_add["age"] = input("添加员工的年龄：")
employee_add["position"] = input("添加员工的职位：")
employee_records[f"{input("添加员工的工号：")}"] = employee_add
print(employee_records)
del employee_records[f"{input("要删除员工的工号：")}"]
print(employee_records)
