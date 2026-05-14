'''
# 死循环：没有循环的结束条件，让循环一直执行下去的过程就是死循环
# 应用场景：可以把死循环与input相结合，实现高级的应用程序
'''
while True:
    print('---------------------------')
    print(' 欢迎使用黑马程序员学生管理系统 ')
    print(' 1、添加学生信息 ')
    print(' 2、修改学生信息 ')
    print('---------------------------')

    usernum = int(input('请输入您要执行操作的编号：'))

    if usernum == 1:
        print('添加学生信息')
        break
    elif usernum == 2:
        print('修改学生信息')
        break