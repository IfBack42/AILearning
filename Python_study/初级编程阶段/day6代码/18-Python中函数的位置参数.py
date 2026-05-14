'''
理论上，在函数定义时，我们可以为其定义多个参数。但是在函数调用时，我们也应该传递多个参数，正常情况，其要一一对应。
而且位置不能改变，我们把这种参数称之为位置参数。
'''
def user_info(name, age, address):
    print(name)
    print(age)
    print(address)

# 调用user_info函数
user_info('Tom', 23, 'America')