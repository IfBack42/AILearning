"""
题目 求s=a+aa+aaa+aaaa+aa…a的值，
其中a是一个数字。
例如2+22+222+2222+22222(此时共有5个数相加)，
几个数相加由键盘控制。
"""
# 先决定a的值
a = input("输入a的值")
# 用循环来控制1 2 ......n 个a相加
n = int(input("输入要几个数相加"))
# 曹一个列表来装a
list_a = []
# 用列表和循环来把1......到n个a装到列表
for i in range(1,n + 1):
    list_a.append(a * i)
print(list_a)
sum = 0
# 再用列表的相关操作和循环来把列表里的值加起来
for i in list_a:
    i = int(i)
    sum += i
print(sum)