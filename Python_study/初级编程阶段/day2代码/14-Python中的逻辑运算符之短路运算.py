# and短路运算
print(3 and 4)  # 4
# or短路运算
print(0 or 1)   # 1
# and短路运算
str1 = ' '      # 在Python语言中，空格也算1个字符（非空）
num1 = 5
print(str1 and num1)  # 5

# 结论：如果逻辑运算符的两边，非纯表达式，则返回结果并不是bool布尔类型的值，而是返回决定整个表达式结果的那个值。