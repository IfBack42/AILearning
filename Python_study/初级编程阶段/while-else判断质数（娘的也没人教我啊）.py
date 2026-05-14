import math
a = int(input("输入一个数判断是否为质数=>"))
i = 1
if a < 1:
    print("a不是质数")
else:
    while i < math.sqrt(a):
        i += 1
        if a % i == 0:
            print("a不是质数")
            break
    else:
        print ("a是质数")







