# 限制外部文件只能调用func1函数
__all__ = ['func1']

def func1():
    print('my_module5模块中的func1函数')

def func2():
    print('my_module5模块中的func2函数')