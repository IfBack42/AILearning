'''
案例：用for循环实现用户登录
① 输入用户名和密码
② 判断用户名和密码是否正确（username='admin'，password='admin888'）
③ 登录仅有三次机会，超过3次会报错

分析：用户登陆情况有3种:
① 用户名错误(此时便无需判断密码是否正确)  -- 登陆失败
② 用户名正确 密码错误 --登陆失败
③ 用户名正确 密码正确 --登陆成功

扩展：每次登录失败时，都弹出提示，您还剩下几次登录机会
'''
trycount = 4
for i in range(3):
    # 更新计数器的值
    trycount -= 1

    username = input('请输入您的登录账号：')
    password = input('请输入您的登录密码：')

    # 判断用户名或密码是否正确
    if username == 'admin':
        # 用户名正确
        if password == 'admin888':
            print('登录成功')
            break
        else:
            print('登录失败，您的密码输入有误！')
            print(f'您还有{trycount-1}次登录机会')

    else:
        # 用户名错误
        print('登录失败，您的用户名输入错误！')
        print(f'您还有{trycount - 1}次登录机会')