# 1、add()：向集合中增加单一的元素
set1 = {10, 20, 30}
set1.add(40)
set1.add(50)
print(set1)

# 2、update() ：向集合中增加序列类型的数据（字符串/列表/元组/字典/集合）
set2 = {'刘备', '关羽'}
list2 = ['张飞', '赵云']
set2.update(list2)
print(set2)

# 3、update()方法与字符串结合使用
set3 = {'刘德华', '张学友'}
set3.update('蔡徐坤')
print(set3)