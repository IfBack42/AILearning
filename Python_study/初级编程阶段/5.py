# a = int(input("请输入一个数"))
# if a > 0 :
#     print("这个数是正数")
# elif a < 0 :
#     print ("这个数是负数")
# else :
#     print ("这个数为0")

# year = int(input("请输入一个年份"))
# if ((year % 4) == 0) and ((year % 100) != 0):
#     print("这一年是闰年")
# elif year % 400 == 0:
#     print("这一年是闰年")
# else:

# a = eval(input("边长a为："))
# b = eval(input("边长b为："))
# c = eval(input("边长c为："))
# if a + b > c and a + c > b and b + c > a:
#     if a == b == c :
#         print("这个三角形为等边三角形")
#     elif a != b and a != c and b != c:
#         if a ** 2 + b ** 2 == c ** 2 or a ** 2 + c ** 2 == b ** 2 or b ** 2 + c ** 2 == a ** 2:
#             print("这个三角形为直角三角形")
#         else:
#             print("这个三角形为普通的三角形")
#     else:
#         print("这个三角形为等腰三角形")
# else:
#     print("这个不是三角形")

#判断是否为征兵对象
'''
【征兵标准】

性别要求：征收男兵

身高标准：男性160cm以上，女性158cm以上。

男性体重：男性不超过90kg，不低于60kg。

视力标准：右眼裸眼视力不低于4.6，左眼裸眼视力不低于4.5
'''
#from ftplib import parse150

# Gender = eval(input("你的性别是:(man:1 or woman:2)"))
# if Gender == 1:
#     height = eval(input("你的身高是(cm):"))
#     if height > 160:
#         weight = eval(input("你的体重是(kg):"))
#         if weight > 60 and weight < 90:
#             ls = eval(input("你的右眼视力为："))
#             rs = eval(input("你的左眼视力为："))
#             if ls > 4.6 and rs > 4.5:
#                 print("你准参军")
#             else:
#                 print("你不准参军")
#         else:
#             print("你不准参军")
#     else:
#         print("你不准参军")
# else:
#     print("你不准参军")

# choice = input("吃饭还是外卖？==>")
# if choice == "吃饭":
#     print("肘！")
# elif choice == "外卖":
#     print("豪！")
# else:
#     print("夏季吧输入我让你飞起来")

# core = eval(input("你的成绩是："))
# if core < 60:
#     print(" 不及格")
# elif 60 <= core < 70:
#     print("及格")
# elif 70 <= core < 80:
#     print("合格")
# elif 80 <= core <90:
#     print("良好")
# elif 90 <= core < 100:
#     print("优秀")

# d = int(input("今天星期几？"))
# if 1 <= d <= 5:
#     print("工作日")
# elif 5 < d <= 7:
#     print(("休息日"))
# else :
#     print("哥们你确定有这一天？")

#
# a1 = int(input("首项为："))
# d = int(input("公差为："))
# n = int(input("项数为："))
# f =a1 * n + 0.5 * n * (n - 1) * d
# print(f)
# print(type(f))

