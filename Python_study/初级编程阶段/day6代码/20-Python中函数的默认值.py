'''
缺省参数也叫默认参数，用于定义函数，为参数提供默认值，
调用函数时可不传该默认参数的值（注意：所有位置参数必须出现在默认参数前，包括函数定义和调用）。
默认值必须放在所有参数的最右边
'''
def user_info(name, age, gender='male'):
    print(name)
    print(age)
    print(gender)

user_info('陈念涛', 23)
user_info('苗青', 21, 'female')
