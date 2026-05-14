'''
① PyCharm本身自带了一个代码提供的功能，当我们输入Python关键字的前几个字符，然后等待，系统会自动提示相关内容
② Ctrl + / ，主要功能代表将光标选中的内容进行快速注释
③ Ctrl + S ，虽然Pycharm可以对代码自动保存，但是强烈建议，每行代码编写完毕后，习惯性的按Ctrl + S保存
④ 撤销与恢复 ，撤销Ctrl + Z
             恢复Ctrl + Y
⑤ 代码自动格式化 ，Ctrl + Alt + L
⑥ 在编写Python代码时，一定要注意代码缩进问题，在Python语言中，缩进代表上下级关系
⑦ Tab可以用于对父子关系进行快速缩进
⑧ Ctrl + D，快速复制当前行到下一行
'''
num1 = 10
num2 = 20


def add2sum(num1, num2):
    return num1 + num2


print(add2sum(num1, num2))
