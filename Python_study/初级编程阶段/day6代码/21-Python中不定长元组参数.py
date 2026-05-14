'''
不定长元组参数，我们可以通过*args对其进行接收，其返回参数args是一个元组
'''
def user_info(*args):
    print(args)
    print(type(args))


user_info('Lucy', 19)
# user_info('Rose', 18, 'female')