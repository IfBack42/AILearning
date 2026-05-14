def logging(fn):
    def inner(*args):
        print("calculating")
        fn(*args)
        return fn(*args)
    return inner
@logging
def sum_(num1,num2):
    return num1 + num2


print(sum_(*(123,234)))
#print(sum_((123,234)))    *星号是解包的作用，不加星号的话元组是一个整体
# 所以*args也是解包的意思，所以这里能用*args接受不定长参数