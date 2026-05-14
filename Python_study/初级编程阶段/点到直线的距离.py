import math
x0 = eval(input("请输入该点的横坐标"))
y0 = eval(input("请输入该点的纵坐标"))
A = eval(input("请输入直线的x系数"))
B = eval(input("请输入直线的y系数"))
C = eval(input("请输入直线的常数"))
L = math.fabs(A * x0 + B * y0 + C) / math.sqrt(A * A + B * B)
print(f"点到直线距离为{L : .2f}")