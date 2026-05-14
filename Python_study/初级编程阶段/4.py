# a = 1
# b = 2
# print (not(a < b))
# print ((a > b) and (a == b))
# print (a and b)
# print ( a or b)
# c = ""


# title = input("商品名称为")
# num = input("商品编号为")
# price = eval(input("商品价格为"))
# n = eval(input("商品数量为"))
# cut = (eval(input("折扣为"))) / 10
# print(f"您购买了{title}商品{n}件，累计原价{price * n}元，现价{price * n * cut}元，累计折扣{cut * 10}折，欢迎下次光临！")
# print((price * n * cut) > 100)


# import math
# a = eval(input("a边长为"))
# b = eval(input("b边长为"))
# c = eval(input("c边长为"))
# d = (a + b + c) / 2
# s = math.sqrt(d * (d - a) * (d - b) * (d - c))


# import math
# r_a = 3
# S_a = math.pi * r_a * r_a
# r_b = 1
# S_b = math.pi * r_b * r_b
# S = S_a - S_b
# print(f"{S : .2f}")



a = 1
b = 2
c = 3

print(not (a > b) or (b > c) and (a < c))
print(not ((a > b) or (b > c)) and (a < c))

