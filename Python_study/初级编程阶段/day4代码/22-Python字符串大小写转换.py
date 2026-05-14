# 接收用户传递过来的用户名和密码，admin and admin888登录成功
username = input('请输入您的登录名称：')
password = input('请输入您的登录密码：')

if username.upper() == 'ADMIN' and password.upper() == 'ADMIN888':
    print('登录成功')
else:
    print('登录失败')