#阶乘
i = 0
n = int(input("几的阶乘=>"))
sum1 = 1
while i < n:
    i += 1
    sum1 = sum1 * i
print(f"{n}的阶乘为{sum1}")