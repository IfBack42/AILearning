# help("keywords")  #关键字
id = 12
name = "itheima"
print(f"姓名{name:s},学号{id:06d}")

weight = 75.7567
print(f"{weight:.2f}")

name = "肖杰"
email = "114514@qq.com"
print(f"姓名：{name:s},联系方式:{email:s}")

# price = 10
# n = int(input("购买的个数"))
# print(f"价格为：{price * n} ")

a = 10
b = 11.4
c = a + b
print(type(c))
print(c)
d = (b / c)
print(type (d))
print(f"{d:.2}")
'''
请注意，最后一个 print 语句实际上会输出两个值，
因为 and 运算符连接了两个表达式。
但由于 d 的值为 0，在布尔上下文中被视为 False，
所以实际上不会打印 d 的值。
如果 d 的值不为 0，那么 and 运算符会返回 d 的值。
and 不是用来打印什么和什么，而是逻辑运算符，用于判断
'''

#
# m = eval(input("上底长度为"))
# n = eval(input("下底长度为"))
# j = eval(input("高为"))
# y = float((m + n) * j / 2)
# print(f"梯形面积为{y : .2f}")

