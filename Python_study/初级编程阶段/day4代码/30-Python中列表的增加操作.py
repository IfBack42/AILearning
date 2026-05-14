# 定义一个列表
xiyou_list = ['唐僧', '孙悟空', '八戒']
# 1、在列表的尾部追加一个新元素
xiyou_list.append('沙僧')
print(xiyou_list)

# 2、使用extend把两个列表进行合并操作
list1 = ['唐僧', '小白龙']
list2 = ['兔子精', '白骨精']
list1.extend(list2)
print(list1)

# 3、使用extend插入一个字符串（特殊）
list3 = ['hello']
list3.extend('python')
print(list3)  # hello python/ # hello p y t h o n

# 4、在指定的位置插入数据
honglou_list = ['林黛玉', '贾母', '贾雨']
honglou_list.insert(1, '宝哥哥')
print(honglou_list)
