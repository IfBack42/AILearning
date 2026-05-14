while True:
    print("输入要运算的数或者“结束”结束")
    x = input()
    if x == "结束":
        break
    else:
        x = eval(x)
        a = input()
        y = eval(input())
        if a == "+":
            print(x + y)
        elif a == "-":
            print(x - y)
        elif a == "*":
            print(x * y)
        elif a == "/":
            print(x / y)
        else:
            print("出大问题")
            break
