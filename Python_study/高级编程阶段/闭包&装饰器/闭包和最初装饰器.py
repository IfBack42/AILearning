#闭包&装饰器
def func1():
    b = 20
    def inner():
        print(b)
    return inner
fn = func1()
fn()

#闭包和nonlocal的理解
def func2():
    summa = 0
    def inner(a):
        nonlocal summa
        summa += a
        print(summa)
    return inner
func = func2()
func(1)
func(2)
func(3)

#装饰器的原理：
#定义一个普通的函数
def xiaojie():
    print("打死肖杰的马")
#定义一个装饰器
def xiaojie2(func):
    #在内部添加函数增加的功能
    def inner():
        print("打死肖杰的跌")
        func()
    return inner
#夺舍xiaojie函数
xiaojie = xiaojie2(xiaojie)
xiaojie()

#装饰器的真正用法
def zz2(funct):
    def inner():
        print("我杀了你的马！！")
        funct()
    return inner

@zz2
def zz1():
    print("敢杀我的马？？")
zz1()


