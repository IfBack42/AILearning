'''
for 临时变量 in 数据序列（字符串/列表/元组/字典/集合）:
    循环体代码
    每次循环时，系统会自动将序列中的元素放入临时变量中，序列中有多少个元素，则整个循环会自动执行多少次

例如：有一个字符串str1 = 'hello'
for i in str1:
    print(i)
    # 由于hello一共有5个字符，所以本循环一共循环5次
    # 第一次循环，获取hello中的h字符放入变量i中，然后print(i)打印h
    # 第二次循环，获取hello中的e字符放入变量i中，然后print(i)打印e
    # 第三次循环，获取hello中的l字符放入变量i中，然后print(i)打印l
    # 第四次循环，获取hello中的l字符放入变量i中，然后print(i)打印l
    # 第五次循环，获取hello中的o字符放入变量i中，然后print(i)打印o
'''
str1 = 'itheima'
for i in str1:
    print(i)