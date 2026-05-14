'''
用户名 + 密码验证案例
'''
username = input('请输入您的登录账号：')
password = input('请输入您的登录密码：')

# 默认账号：admin，默认密码：123456，只要用户输入正确，就提示登录成功，反之，则提示登录失败
if username == 'admin' and password == '123456':
    print('登录成功')
else:
    print('登录失败')