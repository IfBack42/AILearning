'''
for作用：主要用于遍历（循环输出）序列类型的数据（字符串、列表、集合等等）
for...else结构：当for循环正常结束（没有执行break关键字），则自动执行else语句中的缩进代码
'''
str1 = 'itheima'
for i in str1:
    if i == 'e':
        break
    print(i)
else:
    print('当for循环正常结束时要执行的代码')