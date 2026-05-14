'''
Python中函数的嵌套：就是在一个函数中又调用了另外一个函数
'''
def testB():
    print('开始调用testB函数')
    print('testB核心代码')
    print('结束调用testB函数')


def testA():
    print('开始调用testA函数')
    # 调用testB函数
    testB()
    print('结束调用testA函数')


# 调用testA函数
testA()